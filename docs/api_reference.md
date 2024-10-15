
# Whisper API Reference

This document serves as a reference for the Whisper API, detailing the available endpoints and their usage.

## Authentication

### Signup
- **Endpoint:** `/auth/signup/`
- **Method:** `POST`
- **Parameters:**
  - `username`: The username of the user.
  - `password`: The password for the user account.
- **Response:**
  - **Status Code:** `201` on success, `400` on failure.
  - **Example Response:**
    ```json
    {
        "status": 201,
        "id": "user_id"
    }
    ```

### Login
- **Endpoint:** `/auth/login/`
- **Method:** `POST`
- **Parameters:**
  - `username`: The username of the user.
  - `password`: The password for the user account.
- **Response:**
  - **Status Code:** `200` on success, `401` on failure.
  - **Example Response:**
    ```json
    {
        "status": 200,
        "access_token": "token"
    }
    ```

## User Profile

### Get Profile
- **Endpoint:** `/profile/`
- **Method:** `GET`
- **Headers:**
  - `Authorization`: `Bearer <token>`
- **Response:**
  - **Status Code:** `200` on success, `401` if unauthorized.
  - **Example Response:**
    ```json
    {
        "status": 200,
        "data": {
            "username": "Al-Areef",
            "public_key": "public_key_value",
            "ready_to_chat": false
        }
    }
    ```

## Chat Functionality

### Set Ready to Chat
- **Endpoint:** `/ready-to-chat/`
- **Method:** `POST`
- **Headers:**
  - `Authorization`: `Bearer <token>`
- **Parameters:**
  - `Option`: `true` or `false` to indicate readiness to chat.
- **Response:**
  - **Status Code:** `200` on success, `400` on failure.
  - **Example Response:**
    ```json
    {
        "status": 200,
        "message": "Ready to chat status updated."
    }
    ```

### List Online Users
- **Endpoint:** `/online-users/`
- **Method:** `GET`
- **Headers:**
  - `Authorization`: `Bearer <token>`
- **Response:**
  - **Status Code:** `200` on success, `401` if unauthorized.
  - **Example Response:**
    ```json
    {
        "status": 200,
        "public_keys": ["user1_public_key", "user2_public_key"]
    }
    ```

## Error Handling
- All endpoints will return a JSON response with a `status` and an array of `messages` on failure.
- **Example Error Response:**
  ```json
  {
      "status": 400,
      "messages": [{"message": "Error description"}]
  }
  ```

