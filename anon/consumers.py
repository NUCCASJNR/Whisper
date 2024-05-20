#!/usr/bin/env python3


"""
MessageConsumer Documentation

This module defines the MessageConsumer class, which is responsible for handling WebSocket
connections for real-time messaging features in the anon app.It manages authentication,
 message reception, storage, and broadcasting of messages to connected clients.

Classes:
    MessageConsumer: Handles WebSocket connections for real-time messaging.

Methods:
    connect: Establishes a WebSocket connection and processes stored messages.
    disconnect: Closes the WebSocket connection.
    receive: Processes incoming messages from clients.
    chat_message: Sends a message to all clients in the current chat room.
    get_auth_info: Decodes JWT tokens to retrieve user authentication information.
    get_user_by_id: Retrieves a user object by ID.
    save_message: Saves a new message to the database.
    get_stored_messages: Fetches previously stored messages between two users.
    process_stored_messages: Sends previously stored messages to the client upon connection.
"""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async
from django.db.models import Q
from anon.models.message import MainUser, PlainTextMessage
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, filename='app.log')


class MessageConsumer(AsyncWebsocketConsumer):
    """
    Message Consumer
    """

    async def connect(self):
        """
        Connect method
        :return: Nothing
        """
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        token = self.scope.get("query_string").decode().split("Bearer%20")[1]
        auth_info = await self.get_auth_info(token)
        print(auth_info)
        if not auth_info['status']:
            await self.close()
            return f'Error: {auth_info["response"]}'
        self.user_id = auth_info.get('user_id', None)
        self.user = await self.get_user_by_id(auth_info['user_id'])
        self.room_group_name = f"chat_{self.sender_id}_{self.receiver_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.process_stored_messages(self.receiver_id, self.sender_id)

    async def disconnect(self, close_code):
        """
        Disconnect method
        :param close_code: Close code
        :return:
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receives incoming messages
        :param text_data: Incoming message
        :return: Processed messages
        """
        try:
            text_data_json = json.loads(text_data)
            print(text_data, text_data_json)
            message = text_data_json["message"]
            sender = text_data_json.get("sender", self.user.username)
            receiver = str(self.scope['url_route']['kwargs']['receiver_id'])
            send = str(text_data_json.get("sender", self.user.id))
            sender_id = await self.get_user_by_id(send)
            logging.info("Received message '%s' from sender '%s' in room '%s'", message, sender, self.room_group_name)
            response = await self.save_message(message, sender_id, str(self.user_id))
            obj = datetime.fromisoformat(str(response.updated_at))
            time = obj.strftime("%A, %d %B %Y, %I:%M %p")
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                    "time": time
                }
            )
        except json.decoder.JSONDecodeError:
            logging.warning("Received an empty or invalid JSON message")

    async def chat_message(self, event):
        """
        Chat message
        :param event: 
        :return:
        """
        print('event:', event)
        message = event["message"]
        sender = event["sender"]
        logging.info("Sending message '%s' from sender '%s' to room '%s'", message, sender, self.room_group_name)
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "time": event["time"]
        }))

    async def get_auth_info(self, token):
        """
        Get authentication info from a JWT token
        :param token: JWT token
        :return: User ID or False
        """
        try:
            decoded_token = AccessToken(token)
            print(f'Decoded token: {decoded_token}')
            if decoded_token.get("user_id"):
                return {
                    "status": True,
                    "user_id": decoded_token.get("user_id")
                }
            return False
        except Exception as e:
            return {
                "status": False,
                "response": str(e)
            }

    @sync_to_async
    def get_user_by_id(self, user_id):
        """
        Retrieve a user object by ID
        :param user_id: User ID
        :return: User object or None
        """
        try:
            user = MainUser.objects.get(id=user_id)
            return user
        except MainUser.DoesNotExist:
            return None
        except Exception as e:
            return f'Error: {e}'

    @sync_to_async
    def save_message(self, content, sender, receiver):
        """
        Save a new message to the database
        :param content: Content of the message
        :param sender: Sender ID
        :param receiver: Receiver ID
        :return: Saved message object
        """
        try:
            message = PlainTextMessage.custom_save(**{'content': content, 'sender': sender, 'recipient': receiver})
            return message
        except Exception as e:
            logging.error(f"Error saving message: {e}")

    @sync_to_async
    def get_stored_messages(self, recipient_id, sender_id):
        """
        Fetch previously stored messages between two users
        :param recipient_id: Recipient ID
        :param sender_id: Sender ID
        :return: List of message objects
        """
        try:
            messages = PlainTextMessage.objects.filter(
                (Q(recipient=recipient_id) & Q(sender=sender_id)) | (Q(recipient=sender_id) & Q(sender=recipient_id))
            ).order_by('-updated_at')
            return list(messages)
        except ValueError:
            logging.info(f"These users don't have previous chats")
            return []

    async def process_stored_messages(self, recipient_id, sender_id):
        """
        Process and send previously stored messages to the client upon connection
        :param recipient_id: Recipient ID
        :param sender_id: Sender ID
        :return: None
        """
        messages = await self.get_stored_messages(recipient_id, sender_id)
        for message in messages:
            sender_user = await self.get_user_by_id(message.sender_id)
            obj = datetime.fromisoformat(str(message.updated_at))
            time = obj.strftime("%A, %d %B %Y, %I:%M %p")
            await self.send(text_data=json.dumps({
                "message": message.content,
                "sender": sender_user.username if sender_user else "Anonymous",
                "time": time
            }))
