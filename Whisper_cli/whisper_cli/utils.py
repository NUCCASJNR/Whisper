import os


def save_token(username, token):
    """
    Save token with a username as the filename
    params:
        username: username of the user
    """
    TOKEN_FILE = os.path.expanduser(f"~/{username}_whisper_token")
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
