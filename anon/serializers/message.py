#!/usr/bin/env python3

"""Contains message related serializers"""

from rest_framework import serializers
from anon.models.message import PlainTextMessage, Message


class SendMessageSerializer(serializers.ModelSerializer):
    """Serializer for sending encrypted messages"""

    class Meta:
        model = Message
        fields = ('encrypted_content', )


class MessageSerializer(serializers.ModelSerializer):
    """Message Serializer"""

    class Meta:
        model = PlainTextMessage
        fields = ('content', )


class RecieveMessageSerializer(serializers.ModelSerializer):
    """Receive Message Serializer"""
    sender = serializers.CharField()
    content = serializers.CharField()
    # recipient = serializers.SerializerMethodField()

    class Meta:
        model = PlainTextMessage
        fields = ('sender', 'content')
