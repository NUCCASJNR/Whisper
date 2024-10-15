import os
import json


def save_token(username, token):
    """
    Save token with a username as the filename if it's different from the current token.
    Params:
        username: Username of the user.
        token: The new token to save.
    """
    TOKEN_FILE = os.path.expanduser(f"~/{username}_whisper_token")
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            current_token = f.read().strip()
        if current_token == token:
            print(f"Token for {username} is already up to date.")
            return
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    print(f"Token for {username} has been updated.")


def get_token(username):
    """Read the saved token from file."""
    TOKEN_FILE = os.path.expanduser(f"~/{username}_whisper_token")
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return None


def format_response(data, indent=3):
    """Format  API response in JSON format
    Args:
        data: Data to be formatted
        indent: Indentation to be used, default is 3
    """
    return json.dumps(data, indent=indent)
