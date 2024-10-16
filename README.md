
# Whisper CLI Tool

Whisper CLI is a command-line interface tool that allows users to interact with the Whisper application, performing actions like signing up, logging in, setting availability for chat, viewing profiles, and listing active users.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Login](#login)
  - [Signup](#signup)
  - [Ready to Chat](#ready-to-chat)
  - [Profile](#profile)
  - [Active Users](#active-users)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.6+
- `pip` (Python package installer)
- `requests` package for handling HTTP requests

To install the necessary dependencies, run the following command:
```bash
pip install whisper_chat
```

## Usage

Once you have installed the dependencies, you can use the `whisper` command in your terminal to interact with the CLI tool.

### General Command Format

The basic format for using the Whisper CLI is:
```bash
whisper <command> --username <username> --password <password> --option <option>
```

Each command has specific options and flags as described below.

### Signup
To create a new user account:
```bash
whisper signup --username <your-username> --password <your-password>
```

This command registers you as a new user in the application. Ensure that both username and password are provided.

### Login
To log into the application:
```bash
whisper login --username <your-username> --password <your-password>
```

This command logs you in using your credentials and returns an authentication token that will be used in subsequent requests.


### Ready to Chat
To set your availability for chatting:
```bash
whisper ready_to_chat --username <your-username>
```

After running this command, you will be prompted to enter whether you're ready to chat:
- Enter `Yes`, `Y`, or `ON` to mark yourself as available.
- Enter `No`, `N`, or `OFF` to mark yourself as unavailable.

### Profile
To view your profile information:
```bash
whisper profile --username <your-username>
```

This command retrieves and displays details about your profile, such as your username, email, and current availability status.

### Active Users
To view a list of all active users (users who are available for chatting):
```bash
whisper active_users --username <your-username>
```

This command will return a list of all users who are online and ready to chat.

## Commands

The CLI supports the following commands:

| Command         | Description                                       | Required Arguments          | Optional Arguments |
|-----------------|---------------------------------------------------|-----------------------------|--------------------|
| `login`         | Logs into the application                         | `--username`, `--password`  |                    |
| `signup`        | Registers a new user                              | `--username`, `--password`  |                    |
| `ready_to_chat` | Sets your chat availability (ready/not ready)      | `--username`                |                    |
| `profile`       | Displays your profile information                 | `--username`                |                    |
| `active_users`  | Lists all users who are available for chatting     | `--username`                |                    |

### Examples

- **Login**
  ```bash
  whisper login --username Al-Areef --password Wagwan
- **Signup**
  ```bash
  whisper signup --username Al-Areef --password Wagwan
  ```
- **Set Ready to Chat**
  ```bash
  whisper ready_to_chat --username Al-Areef
  ```
  Then you will be prompted to type `Yes/Y` or `No/N` to set your availability.
  
- **View Profile**
  ```bash
  whisper profile --username sAl-Areef
  ```

- **List Active Users**
  ```bash
  whisper active_users --username Al-Areef
  ```

## Contributing

We welcome contributions! If you have any features or improvements, feel free to open an issue or submit a pull request. Make sure to include tests for your new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
