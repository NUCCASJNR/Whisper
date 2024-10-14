import argparse
from whisper_cli.api import WhisperAPI


def main():
    parser = argparse.ArgumentParser(description="Whisper CLI")
    parser.add_argument('command', choices=['login', 'send', 'fetch', 'signup'], help='Command to run')
    parser.add_argument('--message', help='Message to send')
    parser.add_argument('--username', help='Your username')
    parser.add_argument('--password', help='Your password')
    args = parser.parse_args()

    api = WhisperAPI()

    if args.command == 'login':
        api.login(args.username, args.password)
    elif args.command == "signup":
        api.signup(args.username, args.password)
    elif args.command == 'send':
        api.send_message(args.message)
    elif args.command == 'fetch':
        api.fetch_messages()


if __name__ == '__main__':
    main()
