#!/bin/bash

# Function to display the menu
function display_menu {
    echo "============================"
    echo "  Django Project Helper"
    echo "============================"
    echo "Available Commands:"
    echo "mg  - Make Migrations          (Generates migration files for your app)"
    echo "m   - Migrate                  (Applies migrations to the database)"
    echo "rs  - Run Server               (Starts the Django development server)"
    echo "s   - Open Django Shell        (Opens the Django interactive shell)"
    echo "db  - Open Database Shell      (Opens the database shell)"
    echo "v   - Activate Virtual environment  (Activates the Virtual environment)"
    echo "e   - Reload .env              (Reloads .env file changes)"
    echo "q   - Quit                     (Exits the script)"
    echo "============================"
}

# Function to handle the selected option
function handle_option {
    case $1 in
        mg)
            echo "Making migrations... (Generates migration files for your app)"
            python3 manage.py makemigrations
            ;;
        m)
            echo "Applying migrations... (Applies migrations to the database)"
            python3 manage.py migrate
            ;;
        rs)
            echo "Running server... (Starts the Django development server)"
            python3 manage.py runserver
            ;;
        s)
            echo "Opening Django shell... (Opens the Django interactive shell)"
            python3 manage.py shell
            ;;
        db)
            echo "Opening database shell... (Opens the database shell)"
            python3 manage.py dbshell
            ;;
        v) 
            echo "Activating... (Activating virtual environment)"
            source .linux-venv/bin/activate
            ;;
        e)
            echo "Reloading... (Reloading environment variables)"
            source .env
            ;;
        q)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid command. Please try again."
            ;;
    esac
}

# Main script loop
while true; do
    display_menu
    echo -n "Enter a command (mg/m/rs/s/db/v/e/q): "
    read choice
    handle_option $choice
    echo "============================"
done
