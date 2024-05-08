#!/usr/bin/env python3

"""Contains Authentcation related serializers"""

from rest_framework import serializers
from anon.models.user import MainUser


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for handling user signup"""
    class Meta:
        model = MainUser
        fields = ('username', 'password')


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for handling user login"""
    class Meta:
        model = MainUser
        fields = ('username', 'password')
