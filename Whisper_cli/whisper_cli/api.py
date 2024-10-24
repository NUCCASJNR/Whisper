from os import getenv

import requests
from dotenv import load_dotenv

from whisper_cli.utils import format_response, get_token, save_token

load_dotenv()

MODE = getenv("MODE")


class WhisperAPI:
    if MODE == "DEV":
        BASE_URL = "http://localhost:8000/"
    else:
        BASE_URL = getenv("LIVE_URL", "https://whisper-ul4p.onrender.com/")
    if not BASE_URL:
        raise ValueError("LIVE_URL environment variable is not set.")

    def signup(self, username, password):
        response = requests.post(
            f"{self.BASE_URL}auth/signup/",
            data={"username": username, "password": password},
        )
        try:
            response_data = response.json()
            if response_data.get("status") == 201:
                print("Signup successful!")
            else:
                print(f"Signup failed: {response_data}")
        except requests.exceptions.JSONDecodeError:
            print("No valid JSON response from server")

    def login(self, username, password):
        """
        Login function
        """
        response = requests.post(
            f"{self.BASE_URL}auth/login/",
            data={"username": username, "password": password},
        )
        response_data = response.json()
        try:
            if response_data.get("status") == 200:
                print("Login Successful")
                a = save_token(username, response_data.get("access_token"))
                print(a)
            else:
                print(f"Login Failed: {response_data}")
        except Exception as e:
            print(f"Error due to {str(e)}")

    def profile(self, username):
        """
        Gets the profile of a user
        """
        query = requests.post(f"{self.BASE_URL}find-user/", data={"username": username})
        if query.json().get("status") != 200:
            print(format_response((query.json()), 5))
        elif query.json().get("status") == 200 and get_token(username) is None:
            error = {
                "error": f"Login as {username} to view your profile",
                "status": 403,
            }
            form_error = format_response(error, 5)
            print(form_error)
        else:
            token = get_token(username)
            print(f"Username: {username}")
            print(f"Token: {token}")
            if token is None:
                print(f"No token found for user {username}")
                return
            headers = {"Authorization": f"Bearer {token}"}
            print(f"Authorization header: Bearer {token}")
            response = requests.get(
                f"{self.BASE_URL}profile/", headers=headers, data={"username": username}
            )
            try:
                data = response.json()
                print(f"data: {data}")
                if data.get("status") == 200:
                    formatted_data = format_response(data.get("data"), 5)
                    print(f"Profile Details: {formatted_data}")
                else:
                    formatted_error = format_response(
                        data.get("messages")[0].get("message"), 5
                    )
                    print(f"Profile Retrieval failed: {formatted_error}")
            except Exception as e:
                print(f"Error due to: {str(e)}")

    def ready_to_chat(self, username, option):
        """
        Handles user ready to chat option
        Args:
            option: User option
            username: username of the user making the request
        """
        query = requests.post(f"{self.BASE_URL}find-user/", data={"username": username})
        if query.json().get("status") != 200:
            print(format_response((query.json()), 5))
        elif query.json().get("status") == 200 and get_token(username) is None:
            error = {"error": f"Login as {username} to set your status", "status": 403}
            form_error = format_response(error, 5)
            print(form_error)
        else:
            token = get_token(username)
            headers = {"Authorization": f"Bearer {token}"}
            positive = ["ON", "on", "YES", "Yes", "Y", "y", "True"]
            negative = ["OFF", "off", "NO", "No", "N", "n", "False"]
            if option in positive:
                option = True
            elif option in negative:
                option = False
            else:
                print("Ivalid OPtion")
            response = requests.post(
                f"{self.BASE_URL}ready-to-chat/",
                headers=headers,
                data={"Option": option},
            )
            try:
                data = response.json()
                if data.get("status") == 200:
                    formatted_data = format_response(data, 5)
                    print(f"Ready-To-Chat Details: {formatted_data}")
                else:
                    formatted_error = format_response(
                        data.get("messages")[0].get("message"), 5
                    )
                    print(f"Ready to Chat failed: {formatted_error}")
            except Exception as e:
                print(f"Error due to: {str(e)}")

    def list_online_users(self, username):
        """
        Lists all the active users
        Args:
            username: Username of the user making the request
        """
        query = requests.post(f"{self.BASE_URL}find-user/", data={"username": username})
        if query.json().get("status") != 200:
            print(format_response((query.json()), 5))
        elif query.json().get("status") == 200 and get_token(username) is None:
            error = {"error": f"Login as {username} to see active users", "status": 403}
            form_error = format_response(error, 5)
            print(form_error)
        else:
            token = get_token(username)
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.BASE_URL}online-users/", headers=headers)
            try:
                data = response.json()
                if data.get("status") == 200:
                    formatted_data = format_response(data, 5)
                    print(f"Online Users: {formatted_data}")
                else:
                    # Safely check if messages exist and is a list
                    messages = data.get("messages", [])
                    if (
                        messages
                        and isinstance(messages, list)
                        and "message" in messages[0]
                    ):
                        formatted_error = format_response(messages[0].get("message"), 5)
                        print(formatted_error)
                    else:
                        print(f"Unknown error occurred or no users online: {data}")
            except Exception as e:
                print(f"Error due to: {str(e)}")
