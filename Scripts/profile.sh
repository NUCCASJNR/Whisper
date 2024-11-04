#!/bin/bash

# Prompt for the token
read -p "Enter your token: " token

# Make the GET request using curl with the provided token
response=$(curl -s -X GET https://whisper-ul4p.onrender.com/profile \
-H "Authorization: Bearer $token")

# Print the response
echo "Response: $response"
