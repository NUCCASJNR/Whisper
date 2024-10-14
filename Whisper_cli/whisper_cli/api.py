import requests
from whisper_cli.utils import save_token


class WhisperAPI:
    BASE_URL = 'http://localhost:8000'

    def signup(self, username, password):
        response = requests.post(f'{self.BASE_URL}/auth/signup/', data={'username': username, 'password': password})
        try:
            response_data = response.json()
            if response_data.get('status') == 201:
                print("Signup successful!")
                print(f"User ID: {response_data.get('id')}")
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
                res = save_token(username, response_data.get('access_token'))
                print(res)
            else:
                print(f"Login Failed: {response_data}")
        except Exception as e:
            print(f"Error due to {str(e)}")
