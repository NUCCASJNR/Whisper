import os


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
