#!/usr/bin/env python3


# import os
# from base64 import urlsafe_b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Generate RSA key pair
def generate_key_pair(encrypt_private_key=False, password=None):
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    # Convert keys to PEM format strings
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    encryption_algorithm = serialization.NoEncryption()
    if encrypt_private_key and password:
        encryption_algorithm = serialization.BestAvailableEncryption(password.encode())

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
    ).decode("utf-8")

    return {"public_key": public_key_pem, "private_key": private_key_pem}
