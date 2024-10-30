from dotenv import load_dotenv
from os import getenv

load_dotenv()


def generate_websocket_url(semder_id, receiver_id):
    if getenv("MODE") == "DEV":
        domain = "ws://127.0.0.1:8000"
    else:
        domain = getenv("LIVE_URL")
    websocket_url = f"{domain}/ws/chat/{semder_id}/{receiver_id}"
    return websocket_url
