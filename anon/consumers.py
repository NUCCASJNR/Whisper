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
    async def connect(self):
        print("Connect method called")
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        token = self.scope.get("query_string").decode().split("Bearer%20")[1]

        print(f'Token: {token}')
        auth_info = await self.get_auth_info(token)
        print(auth_info)

        if not auth_info:
            await self.close()
            return

        self.user_id = auth_info['user_id']
        self.user = await self.get_user_by_id(auth_info['user_id'])
        print("user:", self.user)
        sender_room_name = f"chat_{self.user_id}"
        receiver_room_name = f"chat_{self.receiver_id}"
        self.room_group_name = f"chat_{self.sender_id}_{self.receiver_id}"
        print("Room Group Name:", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.process_stored_messages(self.receiver_id, self.sender_id)

    async def disconnect(self, close_code):
        print("DisConnect method called")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logging.info("User disconnected with ID: %s", self.user_id)

    async def receive(self, text_data):
        print("Receive method called")
        print(text_data)
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
            message = text_data_json["message"]
            sender = text_data_json.get("sender", self.user.username)
            receiver = str(self.scope['url_route']['kwargs']['receiver_id'])
            send = str(text_data_json.get("sender", self.user.id))
            sender_id = await self.get_user_by_id(send)
            receiver_room_name = f"chat_{receiver}"
            logging.info("Received message '%s' from sender '%s' in room '%s'", message, sender, self.room_group_name)
            response = await self.save_message(message, sender_id, await self.get_user_by_id(receiver))
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
        print(f'Event: {event}')
        print("Chat message method called")
        message = event["message"]
        sender = event["sender"]
        print(sender)
        logging.info("Sending message '%s' from sender '%s' to room '%s'", message, sender, self.room_group_name)
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "time": event["time"]
        }))

    async def get_auth_info(self, token):
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
            return f'Error: {e}'

    @sync_to_async
    def get_user_by_id(self, user_id):
        try:
            user = MainUser.objects.get(id=user_id)
            return user
        except MainUser.DoesNotExist:
            return None
        except Exception as e:
            return f'Error: {e}'

    @sync_to_async
    def save_message(self, content, sender, receiver):
        try:
            message = PlainTextMessage.custom_save(**{'content': content, 'sender': sender, 'recipient': receiver})
            return message
        except Exception as e:
            logging.error(f"Error saving message: {e}")

    @sync_to_async
    def get_stored_messages(self, recipient_id, sender_id):
        try:
            messages = PlainTextMessage.objects.filter(
                (Q(recipient=recipient_id) & Q(sender=sender_id)) | (Q(recipient=sender_id) & Q(sender=recipient_id))
            ).order_by('-updated_at')
            return list(messages)
        except ValueError:
            logging.info(f"These users don't have previous chats")
            return []

    async def process_stored_messages(self, recipient_id, sender_id):
        messages = await self.get_stored_messages(recipient_id, sender_id)
        for message in messages:
            # Assuming get_user_by_id is correctly implemented and returns the user object
            sender_user = await self.get_user_by_id(message.sender_id)
            obj = datetime.fromisoformat(str(message.updated_at))
            time = obj.strftime("%A, %d %B %Y, %I:%M %p")
            await self.send(text_data=json.dumps({
                "message": message.content,
                "sender": sender_user.username if sender_user else "Anonymous",
                "time": time
            }))

