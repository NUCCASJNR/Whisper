import requests
from whisper_cli.utils import save_token, get_token, format_response
from os import getenv
from dotenv import load_dotenv
load_dotenv()

MODE = getenv("MODE")


class WhisperAPI:
    if MODE == 'DEV':
        BASE_URL = 'http://localhost:8000'
    else:
        BASE_URL = getenv("LIVE_URL")

    def signup(self, username, password):
        response = requests.post(f'{self.BASE_URL}auth/signup/', data={'username': username, 'password': password})
        try:
            response_data = response.json()
            if response_data.get('status') == 201:
                print("Signup successful!")
            else:
                print(f"Signup failed: {response_data}")
        except requests.exceptions.JSONDecodeError:
            print("No valid JSON response from server")

    def login(self, username, password):
        """
        Login function
        """
        response = requests.post(f'{self.BASE_URL}/auth/login/', data={'username': username, 'password': password})
        response_data = response.json()
        try:
            if response_data.get('status') == 200:
                print("Login Successful")
                print(f"Token: {response_data.get('access_token')}")
                save_token(username, response_data.get('access_token'))
            else:
                print(f"Login Failed: {response_data}")
        except Exception as e:
            print(f"Error due to {str(e)}")

    def profile(self, username):
        """
        Gets the profile of a user
        """
        token = get_token(username)
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{self.BASE_URL}/profile/', headers=headers)
        try:
            data = response.json()
            if data.get('status') == 200:
                formatted_data = format_response(data.get('data'), 5)
                print(f'Profile Details: {formatted_data}')
            else:
                formatted_error = format_response(data.get('messages')[0].get('message'), 5)
                print(f"Profile Retrieval failed: {formatted_error}")
        except Exception as e:
            print(f"Error due to: {str(e)}")

    def ready_to_chat(self, username, option):
        """
        Handles user ready to chat option
        Args:
            option: User option
            username:
        """
        token = get_token(username)
        headers = {'Authorization': f'Bearer {token}'}
        positive = ['ON', 'on', 'YES', 'Yes', 'Y', 'y', 'True']
        negative = ['OFF', 'off', 'NO', 'No', 'N', 'n', 'False']
        if option in positive:
            option = True
        elif option in negative:
            option = False
        else:
            print('Ivalid OPtion')
        response = requests.post(f'{self.BASE_URL}/ready-to-chat/', headers=headers, data={'Option': option})
        try:
            data = response.json()
            if data.get('status') == 200:
                formatted_data = format_response(data, 5)
                print(f'Ready-To-Chat Details: {formatted_data}')
            else:
                formatted_error = format_response(data.get('messages')[0].get('message'), 5)
                print(f"Ready to Chat failed: {formatted_error}")
        except Exception as e:
            print(f"Error due to: {str(e)}")

    def list_online_users(self, username):
        """
        Lists all the active users
        Args:
            username: Username of the user making the request
        """
        token = get_token(username)
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{self.BASE_URL}/online-users/', headers=headers)
        try:
            data = response.json()
            if data.get('status') == 200 and data.get('public_keys') != []:
                formatted_data = format_response(data, 5)
                print(f'Online Users: {formatted_data}')
            else:
                formatted_error = format_response(data.get('messages')[0].get('message'), 5)
                print(formatted_error)
        except Exception as e:
            print(f"Error due to: {str(e)}")
