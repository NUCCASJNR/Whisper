#!/usr/bin/env python3

"""Message Model For Whisper"""
from anon.models.user import BaseModel, MainUser, models
from cryptography.fernet import Fernet
import base64
from django.conf import settings

key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode())
cipher = Fernet(key)


class Conversation(BaseModel):
    """
    Conversation Model
    """

    name = models.CharField(max_length=150, unique=True)
    participants = models.ManyToManyField(MainUser, related_name="conversations")
    user_pins = models.JSONField(default=dict)

    class Meta:
        db_table = "conversations"

    def set_pin(self, user_id: str, pin: str):
        """
        Encrypts and stores a user's PIN in the user_pins JSON field
        """
        try:
            encrypted_pin = cipher.encrypt(str(pin).encode()).decode()
            # Update the user_pins field
            self.user_pins[str(user_id)] = encrypted_pin
            # Use custom_save to persist the updated instance
            Conversation.custom_save(instance=self, user_pins=self.user_pins)
            return True
        except Exception as e:
            return f"An error occurred: {e}"

    def verify_pin(self, user_id: str, pin: str) -> bool:
        """
        Verifies the user's PIN by decrypting and comparing.
        """
        encrypted_pin = self.user_pins.get(str(user_id))
        if not encrypted_pin:
            return False
        try:
            decrypted_pin = cipher.decrypt(encrypted_pin.encode()).decode()
            print(f"Decrypted pin: {decrypted_pin} Type: {type(decrypted_pin)}")
            return decrypted_pin == str(pin)
        except Exception:
            return False


class Message(BaseModel):
    """
    Message Model
    """

    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        MainUser, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        MainUser, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self):
        return (
            f"Message {self.id} from {self.sender.username} to {self.receiver.username}"
        )

    class Meta:
        ordering = ["created_at"]
        db_table = "messages"


class GroupMessage(BaseModel):
    conversation = models.ForeignKey(
        Conversation, related_name="group_messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        MainUser, related_name="sent_group_messages", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"

    class Meta:
        ordering = ["created_at"]
        db_table = "group_messages"
