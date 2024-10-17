#!/bin/bash

# Define user credentials
USER1="user1"
PASS1="password1"

USER2="user2"
PASS2="password2"

USER3="user3"
PASS3="password3"

# Function to handle signup
signup() {
  echo "Signing up user: $1"
  whisper signup --username "$1" --password "$2"
  echo "-----------------------------------------"
}

# Function to handle login
login() {
  echo "Logging in user: $1"
  whisper login --username "$1" --password "$2"
  echo "-----------------------------------------"
}

# Function to handle ready_to_chat
ready_to_chat() {
  echo "Setting ready_to_chat for user: $1"
  whisper ready_to_chat --username "$1"
  echo "-----------------------------------------"
}

# Function to handle profile
profile() {
  echo "Fetching profile for user: $1"
  whisper profile --username "$1"
  echo "-----------------------------------------"
}

# Function to handle listing active users
active_users() {
  echo "Listing active users for user: $1"
  whisper active_users --username "$1"
  echo "-----------------------------------------"
}

# Run signup, login, and tasks for User 1
signup "$USER1" "$PASS1"
login "$USER1" "$PASS1"
ready_to_chat "$USER1"
profile "$USER1"
active_users "$USER1"

# Run signup, login, and tasks for User 2
signup "$USER2" "$PASS2"
login "$USER2" "$PASS2"
ready_to_chat "$USER2"
profile "$USER2"
active_users "$USER2"

# Run signup, login, and tasks for User 3
signup "$USER3" "$PASS3"
login "$USER3" "$PASS3"
ready_to_chat "$USER3"
profile "$USER3"
active_users "$USER3"

echo "All tasks completed!"
