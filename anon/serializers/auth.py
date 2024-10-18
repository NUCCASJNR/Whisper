#!/usr/bin/env python3

"""Contains Authentication related serializers"""

from rest_framework import serializers

from anon.models.user import MainUser


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for handling user signup"""

    id = serializers.ReadOnlyField()

    class Meta:
        model = MainUser
        fields = ("username", "password", "id")

    def validate_username(self, value):
        """
        Check if the username exists
        """
        if MainUser.find_obj_by(**{"username": value}):
            raise serializers.ValidationError("username Exists")
        return value

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        user = MainUser.custom_save(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for handling user login"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = MainUser
        fields = ("username", "password")
