import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from anon.utils.encrypt import (
    load_public_key,
    load_private_key,
    encrypt_message,
    decrypt_message,
)
from anon.utils.key import generate_key_pair


def test_load_public_key():
    key_pair = generate_key_pair()
    public_key = load_public_key(key_pair["public_key"])
    assert isinstance(public_key, rsa.RSAPublicKey)


def test_load_private_key():
    key_pair = generate_key_pair()
    private_key = load_private_key(key_pair["private_key"])
    assert isinstance(private_key, rsa.RSAPrivateKey)


def test_encrypt_decrypt_message():
    key_pair = generate_key_pair()
    message = "This is a secret message."

    # Encrypt the message using the public key
    encrypted_message = encrypt_message(message, key_pair["public_key"])
    print(f"Message: {encrypted_message}")
    assert isinstance(encrypted_message, bytes)

    # Load the private key
    private_key = load_private_key(key_pair["private_key"])

    # Decrypt the message using the private key
    decrypted_message = decrypt_message(encrypted_message, key_pair["private_key"])
    assert decrypted_message.decode() == message


def test_encrypt_with_invalid_public_key():
    key_pair = generate_key_pair()
    invalid_public_key_pem = key_pair["public_key"] + "invalid"

    message = "This is a secret message."
    try:
        encrypt_message(message, invalid_public_key_pem)
    except Exception as e:
        print(f"Exception raised: {type(e).__name__}, {str(e)}")
        raise


def test_decrypt_with_invalid_private_key():
    key_pair1 = generate_key_pair()
    key_pair2 = generate_key_pair()

    message = "This is a secret message."
    encrypted_message = encrypt_message(message, key_pair1["public_key"])

    with pytest.raises(ValueError):
        decrypt_message(encrypted_message, key_pair2["private_key"])


def test_decrypt_with_wrong_key():
    key_pair1 = generate_key_pair()
    key_pair2 = generate_key_pair()

    message = "This is a secret message."
    encrypted_message = encrypt_message(message, key_pair1["public_key"])

    with pytest.raises(ValueError):
        decrypt_message(encrypted_message, key_pair2["private_key"])


if __name__ == "__main__":
    pytest.main()
