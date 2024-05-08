#!/usr/bin/env python3

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


# Generate RSA key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return {'public_key':
            public_key.public_bytes(
             encoding=serialization.Encoding.PEM,
             format=serialization.PublicFormat.SubjectPublicKeyInfo
            ),
            'private_key': private_key.private_bytes(
             encoding=serialization.Encoding.PEM,
             format=serialization.PrivateFormat.PKCS8,
             encryption_algorithm=serialization.NoEncryption()
            )
            }
