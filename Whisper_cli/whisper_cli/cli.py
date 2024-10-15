import argparse
from whisper_cli.api import WhisperAPI


def main():
    parser = argparse.ArgumentParser(description="Whisper CLI")
    parser.add_argument('command', choices=['login', 'send', 'ready_to_chat', 'signup', 'profile', 'active_users'], help='Command to run')
    parser.add_argument('--message', help='Message to send')
    parser.add_argument('--username', help='Your username')
    parser.add_argument('--password', help='Your password')
    parser.add_argument('--option', help="Ready-To-Chat Option")
    args = parser.parse_args()

    api = WhisperAPI()

    if args.command == 'login':
        api.login(args.username, args.password)
    elif args.command == "ready_to_chat":
        user_input = input('Yes/Y for Turning ON and No/N to Turn off.....:  ')
        api.ready_to_chat(args.username, user_input)
    elif args.command == 'active_users':
        api.list_online_users(args.username)
    elif args.command == 'profile':
        api.profile(args.username)
    elif args.command == "signup":
        api.signup(args.username, args.password)
    elif args.command == 'send':
        api.send_message(args.message)
    elif args.command == 'fetch':
        api.fetch_messages()


if __name__ == '__main__':
    main()
