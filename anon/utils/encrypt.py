from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import hashes


def load_private_key(private_key_bytes: bytes):
    """
    Load private key from PEM-encoded data
    :param private_key_bytes: Private key bytes
    :return: Private key object
    """
    private_key = serialization.load_pem_private_key(private_key_bytes.encode(),
                                                     password=None, backend=default_backend())
    return private_key


def load_public_key(public_key_bytes: bytes):
    """
    Load public key from PEM-encoded data
    :param public_key_bytes: Public key bytes
    :return: Public key object
    """
    public_key = serialization.load_pem_public_key(public_key_bytes.encode(), backend=default_backend())
    return public_key


def encrypt_message(message: str, recipient_public_key: str) -> bytes:
    """
    Encrypt a message using the recipient's public key.
    :param message: The message to encrypt
    :param recipient_public_key: The recipient's public key in PEM format
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


def decrypt_message(encrypted_message: bytes, private_key: str) -> bytes:
    """
    Decrypt a message using the private key.
    :param encrypted_message: The encrypted message
    :param private_key: The private key in PEM format
    :return: Decrypted message
    """
    private_key = load_private_key(private_key)
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message
