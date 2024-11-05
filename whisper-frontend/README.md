# Whisper Chat App

**Whisper** is a secure chat application that allows users to send and receive encrypted messages using public and private key pairs. This project features a frontend built with **React**, **Vite**, **Tailwind CSS**, and **TypeScript**, with a focus on ease of use, security, and customization.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Secure Conversations**: End-to-end encryption using public and private key pairs.
- **User Profiles**: View and manage user profiles with public key information.
- **Chats Management**: View, create, and manage chats in real-time.
- **Users Ready to Chat**: Discover users ready to start a conversation and initiate chats with them.
- **Responsive Design**: Mobile-friendly UI with responsive sidebar, header, and chat window.
- **Customizable Theme**: Modify primary, secondary, and accent colors through Tailwind CSS.
- **Dark Mode Support**: Built-in dark mode with customizable components.
- **Modals for Interactions**: Modals for creating new chats, changing passwords, and more.

## Technologies

- **React**: UI library for building component-based web applications.
- **TypeScript**: Type-safe language to ensure code quality.
- **Vite**: Next-generation frontend tool for fast builds and hot module replacement.
- **Tailwind CSS**: Utility-first CSS framework for rapidly building custom UIs.
- **React Router**: Declarative routing for React applications.
- **React Icons**: Icon library with a variety of customizable icons.
- **Context API**: For managing Apientication and chat state globally.

## Installation

To set up and run the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/whisper-chat.git
   cd whisper-chat
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Set up the environment variables in a `.env` file (if needed).

4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open the app in your browser at `http://localhost:5173`.

## Usage

### User Apientication

- Users must log in using their **username** and **password**.
- The **Profile Page** displays the user’s public key and allows toggling "Ready to Chat" status.
- Users can log out from the profile page.

### Chat Management

- **Chat List**: View all existing chats.
- **New Chat**: Start a new chat using the floating action button.
- **Ready to Chat Page**: View other users who are ready to chat and initiate conversations with them.

### Theme Customization

To customize the app’s theme:

1. Modify the **Tailwind CSS** configuration (`tailwind.config.js`) to adjust primary, secondary, and accent colors.
2. Use these custom colors throughout your components to maintain consistency.

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#1D4ED8',
        secondary: '#1F2937',
        accent: '#F59E0B',
        // Add more color schemes here...
      },
    },
  },
};
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code adheres to the project’s **code style** and **best practices**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
