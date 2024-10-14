import requests


class WhisperAPI:
    BASE_URL = 'http://localhost:8000'  # Replace with your actual API URL if necessary

    def signup(self, username, password):
        response = requests.post(f'{self.BASE_URL}/auth/signup/', data={'username': username, 'password': password})        
        try:
            response_data = response.json()
            # Check the status field in the response JSON
            if response_data.get('status') == 201:
                print("Signup successful!")
                print(f"User ID: {response_data.get('id')}")
            else:
                print(f"Signup failed: {response_data}")
        except requests.exceptions.JSONDecodeError:
            print("No valid JSON response from server")
