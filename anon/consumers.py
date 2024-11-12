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
        logger.info(f"Types: {type(self.sender_id)}: {type(self.receiver_id)}: {type(self.user.id)}")

        # Determine sender and receiver roles
        if str(self.user.id) == self.receiver_id:
            self.actual_receiver_id = self.sender_id
        elif str(self.user.id) == self.sender_id:
            self.actual_receiver_id = self.receiver_id
        else:
            self.actual_receiver_id = self.receiver_id
        self.message_sender = await self.get_user_by_id(self.sender_id)
        self.message_receiver = await self.get_user_by_id(self.actual_receiver_id)
        logger.info(f"Sender: {self.message_sender} Receiver: {self.message_receiver}")
        self.pin_verified = False
        await self.send(text_data=json.dumps({"prompt": "Enter PIN for secure connection"}))

    async def receive(self, text_data):
        """
        Receives incoming messages and handles PIN verification or creation.
        """
        try:
            print(f"Json: {text_data}")
            text_data_json = json.loads(text_data)
            if "pin" in text_data_json:
                pin = text_data_json.get("pin")
                logger.debug("Checking if conversation exists between sender and receiver")
                conversation_exists = await self.conversation_exists(self.message_sender, self.message_receiver)
                logger.debug(f"Conversation exists: {conversation_exists}")

                if conversation_exists:
                    # Existing conversation - verify PIN
                    if await self.verify_pin(self.user_id, pin):
                        await self.send(text_data=json.dumps({"status": "PIN verified"}))
                        logger.info("PIN verified")
                        self.pin_verified = True
                        await self.process_stored_messages(self.sender_id, self.actual_receiver_id)
                    else:
                        await self.send(text_data=json.dumps({"status": "PIN verification failed"}))
                else:
                    convo_res = await self.get_or_create_conversation(str(self.user.id), self.receiver_id)
                    logger.debug(f"Conversation result: {convo_res}")
                    logger.info(f"Message Sender: {self.user.id} and receiver: {self.receiver_id}")
                    res = await self.set_pin(self.user.id, pin)
                    logger.debug(f"Pin set result: {res}")
                    self.pin_verified = True
                    await self.send(text_data=json.dumps({"status": "New conversation created and PIN set"}))

            if self.pin_verified:
                message = text_data_json["message"]
                logger.info(f"Message: {message}")
                message = await self.save_message_async(message)
                if message:
                    obj = datetime.fromisoformat(str(message.updated_at))
                    time = obj.strftime("%A, %d %B %Y, %I:%M %p")
                    await self.channel_layer.group_send(
                        f"chat_{self.sender_id}_{self.receiver_id}",
                        {
                            "type": "chat_message",
                            "message": message.content,
                            "sender": message.sender.username,
                            "time": time,
                        },
                    )
                    await self.channel_layer.group_send(
                        f"chat_{self.receiver_id}_{self.sender_id}",
                        {
                            "type": "chat_message",
                            "message": message.content,
                            "sender": message.sender.username,
                            "time": time,
                        },
                    )
        except Exception as e:
            logger.error(f"Error receiving message: {str(e)}")

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

    @database_sync_to_async
    def conversation_exists(self, user_1, user_2):
        """
        Check if a conversation exists between two users
        :param user_1: User instance (first participant)
        :param user_2: User instance (second participant)
        :return: True if conversation exists, else False
        """
        try:
            conversation = (
                Conversation.objects.filter(participants=user_1)
                .filter(participants=user_2)
                .distinct()
                .first()
            )
            if conversation:
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking conversation existence: {e}")
            return False

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

    @sync_to_async
    def set_pin(self, user_id: str, pin: str):
        """
        Encrypts and stores a user's PIN in the user_pins JSON field
        params:
            user_id: The user's ID.
            pin: The user's PIN
        """
        # Retrieve the specific conversation instance for this user
        try:
            conversation = Conversation.objects.filter(participants=user_id).first()
            logger.info(f"Fethched Conversation: {conversation}")
            if conversation:
                conversation.set_pin(user_id, pin)
                logger.info(f"PIN set successfully for user {user_id}")
                return f"PIN set successfully for user {user_id}"
            logger.info("No conversation found")
            return "No conversation found"
        except Exception as e:
            logger.debug(f"Error setting PIN: {e}")
            return str(e)

    @sync_to_async
    def verify_pin(self, user_id: str, pin: str) -> bool:
        """
        Verify the user's PIN by decrypting and comparing.
        params:
            user_id: The user's ID.
            pin: The user's PIN.
        """
        # Retrieve the specific conversation instance for this user
        try:
            conversation = Conversation.objects.filter(participants__id=user_id).first()
            if conversation:
                return conversation.verify_pin(user_id, pin)
            return False
        except Conversation.DoesNotExist:
            return False

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
