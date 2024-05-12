#!/usr/bin/env python3

"""Contains functions for encrypting an decrypting messages"""


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding


def load_public_key(public_key_bytes):
    """
    Load public key from PEM-encoded data
    :param public_key_bytes: Public key bytes
    :return: Public key object
    """
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    return public_key


def load_private_key(private_key_bytes: bytes):
    """
    Load private key from PEM-encoded data
    :param private_key_bytes: Private key bytes
    :return: Private key object
    """
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())
    return private_key


def encrypt_message(message, recipient_public_key):
    """
    Encrypt message using recipient's public key
    :param message:
    :param recipient_public_key: Public key bytes
    :return: Encrypted message
    """
    public_key = load_public_key(recipient_public_key)
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message


def decrypt_message(encrypted_message, private_key):
    """
    Decrypt message using private key
    :param encrypted_message: Encrypted message
    :param private_key: recipient private key
    :return: Decrypted message
    """
    decrypted_message = private_key.decrypt(
        encrypted_message,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message
