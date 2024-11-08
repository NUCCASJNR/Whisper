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
from datetime import datetime

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import AccessToken

from anon.models.key import PublicKeyDirectory
from anon.models.message import Conversation, MainUser, Message

logger = logging.getLogger("apps")


class MessageConsumer(AsyncWebsocketConsumer):
    """
    Message Consumer
    """

    async def connect(self):
        """
        Connect method
        :return: Nothing
        """
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        headers = self.scope.get("headers")
        token = await self.extract_auth_token(headers)
        logger.info(f"Type of Headers: {type(headers)}")
        logger.info(f"Extraction Result: {token}")
        logger.info(f"B: {b'authorization' in dict(headers)}")

        if not token:
            logger.error("Authorization header not found.")
            await self.close(code=4002)
            return None
        else:
            auth_info = await self.get_auth_info(token)
            logger.debug(f"Auth Info: {auth_info}")

        if not auth_info["status"]:
            await self.close()
            return f'Error: {auth_info["response"]}'

        self.user_id = auth_info.get("user_id", None)
        self.user = await self.get_user_by_id(auth_info["user_id"])

        if not self.user:
            await self.close()
            return "Error: User not found"

        self.group_names = [
            f"chat_{self.sender_id}_{self.receiver_id}",
            f"chat_{self.receiver_id}_{self.sender_id}",
        ]

        for group_name in self.group_names:
            await self.channel_layer.group_add(group_name, self.channel_name)
            logger.info(f"Room Group Name: {group_name}")
        await self.accept()

        # Determine sender and receiver roles
        if str(self.user.id) == self.receiver_id:
            self.actual_receiver_id = self.sender_id
        else:
            self.actual_receiver_id = self.receiver_id
        self.message_sender = await self.get_user_by_id(self.sender_id)
        self.message_receiver = await self.get_user_by_id(self.actual_receiver_id)
        await self.send(text_data=json.dumps({"prompt": "Enter PIN for secure connection"}))

        re = await self.process_stored_messages(self.sender_id, self.actual_receiver_id)
        print("messages:", re)

    async def disconnect(self, close_code):
        """
        Disconnect method
        :param close_code: Close code
        :return:
        """
        for group_name in self.group_names:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receives incoming messages
        :param text_data: Incoming message
        :return: Processed messages
        """
        try:
            print(f"Json: {text_data}")
            text_data_json = json.loads(text_data)
            logger.info(f"Json data: {text_data_json}")
            message = text_data_json["message"]
            sender = text_data_json.get("sender", self.user.username)

            # Save the message
            response = await self.save_message_async(message)
            logger.info(f"response: {response}")
            if response is not None:
                obj = datetime.fromisoformat(str(response.updated_at))
                time = obj.strftime("%A, %d %B %Y, %I:%M %p")
                for group_name in self.group_names:
                    await self.channel_layer.group_send(
                        group_name,
                        {
                            "type": "chat_message",
                            "message": message,
                            "sender": sender,
                            "time": time,
                        },
                    )
            else:
                logger.error("Failed to save message")
        except json.decoder.JSONDecodeError as text_data:
            logger.warning(f"Received an empty or invalid JSON message: {text_data}")
        except Exception as e:
            logger.error(f"Error processing received message: {e}")

    async def chat_message(self, event):
        """
        Chat message
        :param event:
        :return:
        """
        message = event["message"]
        sender = event["sender"]
        logger.info(f"sender: {sender} message{message}")
        # for group_name in self.group_names:
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "time": event["time"]}
            )
        )

    @database_sync_to_async
    def get_stored_messages_sync(self, user_1, user_2):
        """
        Synchronously get all the stored previous messages in a conversation
        """
        try:
            conversation = (
                Conversation.objects.filter(participants=user_1)
                .filter(participants=user_2)
                .distinct()
                .first()
            )
            if conversation:
                messages = Message.objects.filter(conversation_id=conversation.id)
                print(messages)
                return list(messages)
            else:
                return []
        except ValueError:
            logging.info("These users don't have previous chats")
            return []

    async def get_stored_messages(self, user1, user_2):
        """
        Asynchronously fetch stored messages by calling the sync method
        """
        messages = await self.get_stored_messages_sync(user1, user_2)
        return messages

    async def process_stored_messages(self, user_1, user_2):
        """
        Process the stored messages and display them upon successful connection
        """
        messages = await self.get_stored_messages(user_1, user_2)
        for message in messages:
            obj = datetime.fromisoformat(str(message.updated_at))
            time = obj.strftime("%A, %d %B %Y, %I:%M %p")
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message.content,
                        "time": time,
                    }
                )
            )

    @database_sync_to_async
    def confirm_convo_participant(self, user_id, convo_id):
        """
        Confirms if a user is a participant in a conversation before granting access.
        """
        convo = Conversation.custom_get(id=convo_id)

        if convo:
            if convo.participants.filter(id=user_id).exists():
                return True
            else:
                return False
        return False

    @database_sync_to_async
    def get_or_create_conversation(self, user_1, user_2):
        """
        Get or create a conversation between two users.
        :param user_1: User instance (first participant)
        :param user_2: User instance (second participant)
        :return: Conversation object
        """
        try:
            # Get an existing conversation where both users are participants
            conversation = (
                Conversation.objects.filter(participants=user_1)
                .filter(participants=user_2)
                .distinct()
                .first()
            )

            if conversation:
                return conversation
            else:
                # If no conversation exists, create a new one
                conversation = Conversation.objects.create()
                conversation.participants.add(user_1, user_2)
                conversation.save()
                return conversation
        except Exception as e:
            logging.error(f"Error creating or retrieving conversation: {e}")
            return None

    # @database_sync_to_async
    async def save_message_async(self, content):
        try:
            # Fetch the conversation asynchronously
            conversation = await self.get_or_create_conversation(
                self.message_sender, self.message_receiver
            )
            logger.info(f"Fetched Comvo: {conversation}")

            # Save the message asynchronously
            message = await sync_to_async(Message.objects.create)(
                conversation_id=conversation.id,
                sender=self.message_sender,
                receiver=self.message_receiver,
                content=content,
            )
            logger.info(f"Saved: {message}")
            return message
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None

    async def extract_auth_token(self, headers):
        for header in headers:
            if header[0] == b"authorization":
                auth_header = header[1].decode("utf-8")
                if auth_header.startswith("Bearer "):
                    return auth_header[len("Bearer "):]
        return None

    async def get_auth_info(self, token):
        """
        Get authentication info from a JWT token
        :param token: JWT token
        :return: User ID or False
        """
        try:
            decoded_token = AccessToken(token)
            if decoded_token.get("user_id"):
                return {"status": True, "user_id": decoded_token.get("user_id")}
            return False
        except Exception as e:
            return {"status": False, "response": str(e)}

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
            return f"Error: {e}"

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
            return {"error": "No such user found", "status": 404}
