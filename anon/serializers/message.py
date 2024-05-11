#!/usr/bin/env python3

"""Contains message related serializers"""

from rest_framework import serializers
from anon.models.message import PlainTextMessage


class MessageSerializer(serializers.ModelSerializer):
    """Message Serializer"""
    recipient = serializers.CharField()

    class Meta:
        model = PlainTextMessage
        fields = ('recipient', 'content')


class RecieveMessageSerializer(serializers.ModelSerializer):
    """Receive Message Serializer"""
    sender = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = PlainTextMessage
        fields = ('sender', 'content')
