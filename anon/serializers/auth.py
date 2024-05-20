#!/usr/bin/env python3

"""Contains Authentcation related serializers"""

from rest_framework import serializers
from anon.models.user import MainUser


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for handling user signup"""
    class Meta:
        id = serializers.ReadOnlyField()
        model = MainUser
        fields = ('username', 'password', 'id')


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for handling user login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = MainUser
        fields = ('username', 'password')
