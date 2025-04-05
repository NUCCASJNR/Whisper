#!/bin/bash

# Prompt for username
read -p "Enter your username: " username

# Prompt for password
read -sp "Enter your password: " password
echo

# Make the POST request using curl
response=$(curl -s -X POST https://whisper-ul4p.onrender.com/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "'"$username"'", "password": "'"$password"'"}')

# Print the response
echo "Response: $response"

