#!/usr/bin/env python3

"""Contains model for storing users keyys"""

from anon.models.user import BaseModel, models, MainUser
from uuid import uuid4


class EncryptionKey(BaseModel):
    """Model for storing users encrypted key"""
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='private_key')
    private_key = models.TextField()

    class Meta:
        db_table = 'encryption_keys'


class PublicKeyDirectory(BaseModel):
    """PublicKey Directory models for storing users public keys"""
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='public_key_directory')
    public_keys = models.JSONField(default=dict)

    class Meta:
        db_table = 'public_keys'

    def update_public_key(self, user_id: uuid4, public_key: bytes):
        """
        Update a user's public key
        :param user_id: Id of the user whose public key to be updated
        :param public_key: New public key of the user
        :return: Updated public key
        """
        self.public_keys[user_id] = public_key
        self.save()

    def remove_public_key(self, user_id: uuid4):
        """
        Deletes a user public key from the public key directory
        :param user_id:
        :return: None
        """
        if user_id in self.public_keys:
            del self.public_keys[user_id]
            self.save()

    def get_public_key(self, user_id):
        """
        Retrieves a user public key
        :param user_id: User id
        :return: The user public key
        """
        return self.public_keys.get(user_id)
