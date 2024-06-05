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
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async
from django.db.models import Q
from anon.models.message import MainUser, PlainTextMessage, Message
from datetime import datetime
from anon.utils.encrypt import encrypt_message, decrypt_message
from anon.models.key import PublicKeyDirectory, EncryptionKey
from django.core.exceptions import ObjectDoesNotExist
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

        if not auth_info['status']:
            await self.close()
            return f'Error: {auth_info["response"]}'

        self.user_id = auth_info.get('user_id', None)
        self.user = await self.get_user_by_id(auth_info['user_id'])

        if not self.user:
            await self.close()
            return 'Error: User not found'

        self.room_group_name = f"chat_{self.sender_id}_{self.receiver_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Determine sender and receiver roles
        if str(self.user.id) == self.receiver_id:
            self.actual_receiver_id = self.sender_id
        else:
            self.actual_receiver_id = self.receiver_id

        re = await self.process_stored_messages(str(self.user.id), self.actual_receiver_id)
        print("messages:", re)

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
            message = text_data_json["message"]
            sender = text_data_json.get("sender", self.user.username)
            if str(self.user.id) == self.sender_id:
                self.message_sender = self.sender_id
                self.message_receiver = self.receiver_id
            elif str(self.user.id) == self.receiver_id:
                self.message_sender = self.receiver_id
                self.message_receiver = self.sender_id
            else:
                logging.error("User ID does not match sender or receiver")
                return
            res = await self.get_user_public_key(self.message_receiver)
            result = encrypt_message(message, res)
            print(result)
            response = await self.save_message_async(message, self.message_sender, self.message_receiver)
            if response is not None:
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
            else:
                logging.error("Failed to save message")
        except json.decoder.JSONDecodeError:
            logging.warning("Received an empty or invalid JSON message")
        except Exception as e:
            logging.error(f"Error processing received message: {e}")

    async def chat_message(self, event):
        """
        Chat message
        :param event:
        :return:
        """
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

    async def save_message_async(self, content, sender_id, receiver_id):
        """
        Async wrapper for save_message
        """
        return await sync_to_async(self.save_message)(content, sender_id, receiver_id)

    def save_message(self, content, sender_id, receiver_id):
        """
        Save a new message to the database
        :param content: Content of the message
        :param sender_id: Sender ID
        :param receiver_id: Receiver ID
        :return: Saved message object
        """
        try:
            sender = MainUser.custom_get(id=sender_id)
            receiver = MainUser.custom_get(id=receiver_id)
            receiver_key = self.get_user_public_key_sync(receiver_id)
            encrypted_message = encrypt_message(content, receiver_key)
            message = Message.custom_save(encrypted_content=encrypted_message, sender=sender, recipient=receiver)
            logging.info(f'save response: {message}')
            return message
        except MainUser.DoesNotExist:
            logging.error("Sender or recipient does not exist")
            return None
        except Exception as e:
            logging.info(f"Error saving message: {e}")
            return None

    @sync_to_async
    def get_stored_messages(self, recipient_id, sender_id):
        """
        Fetch previously stored messages between two users
        :param recipient_id: Recipient ID
        :param sender_id: Sender ID
        :return: List of message objects
        """
        try:
            messages = Message.objects.filter(
                (Q(recipient=recipient_id) & Q(sender=sender_id)) | (Q(recipient=sender_id) & Q(sender=recipient_id))
            ).order_by('-updated_at')
            return list(messages)
        except ValueError:
            logging.info(f"These users don't have previous chats")
            return []

    async def process_stored_messages(self, user_id, other_user_id):
        """
        Process and send previously stored messages to the client upon connection
        :param user_id: User ID (either sender or receiver)
        :param other_user_id: Other user ID (either receiver or sender)
        :return: None
        """
        messages = await self.get_stored_messages(user_id, other_user_id)
        for message in messages:
            sender_user = await self.get_user_by_id(message.sender_id)
            obj = datetime.fromisoformat(str(message.updated_at))
            time = obj.strftime("%A, %d %B %Y, %I:%M %p")

            # Convert bytes to Base64 encoded string
            encrypted_content_base64 = base64.b64encode(message.encrypted_content).decode('utf-8')

            await self.send(text_data=json.dumps({
                "message": encrypted_content_base64,
                "sender": sender_user.username if sender_user else "Anonymous",
                "time": time
            }))

    async def get_user_public_key(self, user_id):
        """
        Async wrapper for get_user_public_key_sync
        """
        return await sync_to_async(self.get_user_public_key_sync)(user_id)

    def get_user_public_key_sync(self, user_id):
        """
        Fetches a user public key
        :param user_id: ID of the user whose key is to be fetched
        :return: Key of the user else None
        """
        try:
            user = MainUser.custom_get(id=user_id)
            receiver_public_key = PublicKeyDirectory.custom_get(user=user)
            return receiver_public_key.public_keys.get(str(user.id))
        except ObjectDoesNotExist:
            return ({
                "error": "No such user found",
                "status": 404
            })
