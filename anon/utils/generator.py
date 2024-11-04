from os import getenv

from dotenv import load_dotenv
from django.contrib.auth.hashers import make_password, check_password
from anon.models.message import Conversation

load_dotenv()


def generate_websocket_url(semder_id, receiver_id):
    """
    Generate websocket URL
    Args:
        semder_id (str): Sender ID
        receiver_id (str): Receiver ID
    Returns:
        str: Websocket URL
    """
    if getenv("MODE") == "DEV":
        domain = "ws://127.0.0.1:8000/"
    else:
        domain = getenv("LIVE_URL")
    websocket_url = f"wss://{domain}ws/chat/{semder_id}/{receiver_id}"
    return websocket_url


def set_user_pin(conversation, user_id, pin):
    """
    Set user pin in conversation
    Args:
        conversation (Conversation): Conversation instance
        user_id (str): User ID
        pin (int): User pin
    """
    try:
        convo = Conversation.custom_get(**{"id": conversation})
        if convo:
            hashed_pin = make_password(pin)
            convo.user_pins[user_id] = hashed_pin
            convo.save()
        else:
            raise Exception("Conversation not found")
    except Exception as e:
        print(f"Failed to set user pin: {e}")


def verify_user_pin(conversation, user_id, pin):
    """
    Verify user pin in conversation
    Args:
        conversation (Conversation): Conversation instance
        user_id (str): User ID
        pin (int): User pin
    Returns:
        bool: True if pin is verified, False otherwise
    """
    try:
        convo = Conversation.custom_get(**{"id": conversation})
        if convo:
            hashed_pin = convo.user_pins.get(user_id)
            return check_password(pin, hashed_pin)
        else:
            raise Exception("Conversation not found")
    except Exception as e:
        print(f"Failed to verify user pin: {e}")
        return False
