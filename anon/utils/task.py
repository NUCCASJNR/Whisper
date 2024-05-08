#!/usr/bin/env python3

"""Handles All Asynchronous tasks"""

from anon.utils.key import generate_key_pair
from celery import shared_task
from uuid import uuid4
from anon.models.key import EncryptionKey, PublicKeyDirectory, MainUser
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_key_async(user_id: uuid4):
    """
    Generate key pair
    :param user_id: Id of the user that owns the key
    :return:  Result indicating success or failure
    """
    try:
        user = MainUser.custom_get(**{'id': user_id})
        key = generate_key_pair()
        private_key = key['private_key']
        public_key = key['public_key']
        print('Operation about to start!!!')
        EncryptionKey.custom_save(**{'user': user, 'private_key': private_key})
        PublicKeyDirectory.custom_save(**{'user': user, 'public_keys': {str(user.id):
                                                                        public_key.decode('utf-8')}})
        logger.error({'success': True, 'message': f'Keys generated successfully for user {user_id}'})
    except Exception as e:
        logger.error({'success': False, 'message': f'Error generating keys for user {user_id}: {str(e)}'})
