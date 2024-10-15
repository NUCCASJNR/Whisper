import argparse
from whisper_cli.api import WhisperAPI
import logging
import sys


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def handle_login(api, username, password):
    """
    Handle user login.
    """
    if not username or not password:
        logging.error("Username and password are required for login.")
        sys.exit(1)
    try:
        api.login(username, password)
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        sys.exit(1)


def handle_ready_to_chat(api, username):
    """
    Handle setting user ready-to-chat option.
    """
    user_input = input('Type Yes/Y to Turn ON and No/N to Turn OFF: ')
    try:
        api.ready_to_chat(username, user_input)
    except Exception as e:
        logging.error(f"Error during ready_to_chat: {str(e)}")
        sys.exit(1)


def handle_profile(api, username):
    """
    Handle fetching user profile.
    """
    if not username:
        logging.error("Username is required to fetch profile.")
        sys.exit(1) 
    try:
        api.profile(username)
    except Exception as e:
        logging.error(f"Error during profile fetch: {str(e)}")
        sys.exit(1)


def handle_active_users(api, username):
    """
    Handle listing online users.
    """
    if not username:
        logging.error("Username is required to list active users.")
        sys.exit(1)    
    try:
        api.list_online_users(username)
    except Exception as e:
        logging.error(f"Error during active users fetch: {str(e)}")
        sys.exit(1)


def handle_signup(api, username, password):
    """
    Handle user signup.
    """
    if not username or not password:
        logging.error("Username and password are required for signup.")
        sys.exit(1)

    try:
        api.signup(username, password)
    except Exception as e:
        logging.error(f"Error during signup: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to handle CLI commands.
    """
    parser = argparse.ArgumentParser(description="Whisper CLI Tool")
    parser.add_argument('command', choices=['login', 'ready_to_chat', 'signup', 'profile', 'active_users'], help='Command to run')

    parser.add_argument('--username', help='Your username', required=True)
    parser.add_argument('--password', help='Your password')

    args = parser.parse_args()
    api = WhisperAPI()

    # Command handling
    if args.command == 'login':
        handle_login(api, args.username, args.password)

    elif args.command == "ready_to_chat":
        handle_ready_to_chat(api, args.username)

    elif args.command == 'profile':
        handle_profile(api, args.username)
    elif args.command == 'active_users':
        handle_active_users(api, args.username)

    elif args.command == 'signup':
        handle_signup(api, args.username, args.password)


if __name__ == '__main__':
    main()
