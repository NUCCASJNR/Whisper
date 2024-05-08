#!/usr/bin/env python3

"""Message Model For Whisper"""
from anon.models.user import BaseModel, models, MainUser


class Message(BaseModel):
    """
    Message Model
    """
    sender = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField()
    encrypted_session_key = models.BinaryField()
    is_read = models.BooleanField(default=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        """
        String representation of the message.
        """
        return f"From: {self.sender.username} | To: {self.recipient.username} | Content: {self.content}"
