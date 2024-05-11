#!/usr/bin/env python3

"""Profile Serializer"""

from rest_framework import serializers
from anon.models.user import MainUser
from anon.models.key import PublicKeyDirectory
from django.core.exceptions import ObjectDoesNotExist


class ProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer
    """
    public_key = serializers.SerializerMethodField()
    username = serializers.CharField(required=True)

    class Meta:
        model = MainUser
        fields = ('username', 'public_key', 'ready_to_chat')
    
    def get_public_key(self, obj):
        """
        Get the public key of the  current user
        :param obj:  User object
        :return: Public key else None
        """
        try:
            public_key = PublicKeyDirectory.custom_get(**{'user_id': obj.id}).public_keys
            return public_key.get(str(obj.id))
        except ObjectDoesNotExist:
            return 'Not found'


class ReadyToChatSerializer(serializers.Serializer):
    """
    ReadyToChat Serializer
    """
    
    class Meta:
        model = MainUser
        fields = ('ready_to_chat', )
