#!/bin/bash

# Prompt for username
read -p "Enter your username: " username

# Prompt for password
read -sp "Enter your password: " password
echo

# Make the POST request using curl
response=$(curl -s -X POST http://127.0.0.1:8000/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username": "'"$username"'", "password": "'"$password"'"}')

# Print the response
echo "Response: $response"

