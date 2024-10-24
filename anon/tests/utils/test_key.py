import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from anon.utils.key import generate_key_pair


def test_generate_key_pair():
    keys = generate_key_pair()

    # Check if keys are returned
    assert "public_key" in keys
    assert "private_key" in keys

    public_key_pem = keys["public_key"]
    private_key_pem = keys["private_key"]

    # Check if keys are in PEM format
    assert public_key_pem.startswith("-----BEGIN PUBLIC KEY-----")
    assert public_key_pem.endswith("-----END PUBLIC KEY-----\n")

    assert private_key_pem.startswith("-----BEGIN PRIVATE KEY-----")
    assert private_key_pem.endswith("-----END PRIVATE KEY-----\n")

    # Load the keys to ensure they are valid
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )

    assert isinstance(public_key, rsa.RSAPublicKey)
    assert isinstance(private_key, rsa.RSAPrivateKey)


def test_key_length():
    keys = generate_key_pair()
    private_key_pem = keys["private_key"]
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )
    assert private_key.key_size == 2048


def test_public_exponent():
    keys = generate_key_pair()
    private_key_pem = keys["private_key"]
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )
    public_numbers = private_key.public_key().public_numbers()
    assert public_numbers.e == 65537


def test_encrypted_private_key():
    password = "my_strong_password"
    keys = generate_key_pair(encrypt_private_key=True, password=password)
    private_key_pem = keys["private_key"]

    # Check if private key is encrypted
    assert "ENCRYPTED" in private_key_pem

    # Load the private key with the password
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=password.encode()
    )
    assert isinstance(private_key, rsa.RSAPrivateKey)


def test_key_pair_match():
    keys = generate_key_pair()
    public_key_pem = keys["public_key"]
    private_key_pem = keys["private_key"]

    # Load the private key and derive the public key from it
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )
    derived_public_key = private_key.public_key()

    # Load the public key from PEM
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))

    # Compare the public numbers
    assert public_key.public_numbers() == derived_public_key.public_numbers()


def test_sign_and_verify():
    keys = generate_key_pair()
    private_key_pem = keys["private_key"]
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )

    message = b"A message I want to sign"
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )

    public_key = private_key.public_key()
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
    except InvalidSignature:
        pytest.fail("Signature verification failed")


if __name__ == "__main__":
    pytest.main()
