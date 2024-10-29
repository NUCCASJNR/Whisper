#!/usr/bin/env python3

"""Message Model For Whisper"""
from anon.models.user import BaseModel, MainUser, models


class Conversation(BaseModel):
    """
    Conversation Model
    """
    name = models.CharField(max_length=150, unique=True)
    participants = models.ManyToManyField(MainUser, related_name='conversations')

    class Meta:
        db_table = "conversatiions"


class Message(BaseModel):
    """
    Message Model
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(MainUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MainUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['created_at']
        db_table = "messages"


class GroupMessage(BaseModel):
    conversation = models.ForeignKey(Conversation, related_name='group_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(MainUser, related_name='sent_group_messages', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"

    class Meta:
        ordering = ['created_at']
        db_table = "group_messages"
