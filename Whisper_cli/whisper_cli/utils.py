import json
import os


def save_token(username, token):
    """
    Save token with a username as the filename, deleting any existing file before
    creating and saving the new token.
    Params:
        username: Username of the user.
        token: The new token to save.
    """
    TOKEN_FILE = os.path.expanduser(f"~/.{username}_whisper_token")
    print(f"Token file path: {TOKEN_FILE}")
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print(f"Old token file for {username} has been deleted.")
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    print(f"Token for {username} has been updated with the new token.")


def get_token(username):
    """Read the saved token from file."""
    TOKEN_FILE = os.path.expanduser(f"~/.{username}_whisper_token")
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None


def format_response(data, indent=3):
    """Format  API response in JSON format
    Args:
        data: Data to be formatted
        indent: Indentation to be used, default is 3
    """
    return json.dumps(data, indent=indent)
