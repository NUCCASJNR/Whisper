#!/bin/bash

# Prompt for the token
read -p "Enter your token: " token

# Make the GET request using curl with the provided token
response=$(curl -s -X GET http://127.0.0.1:8000/profile/ \
-H "Authorization: Bearer $token")

# Print the response
echo "Response: $response"
