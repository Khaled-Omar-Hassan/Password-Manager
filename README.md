# Password Manager with Login/Registration

This repository contains a Python-based password manager application with a graphical user interface (GUI) that includes user login and registration functionality. The password manager allows users to generate secure passwords, save them, and search for existing passwords.

## Features

- User login and registration.
- Password generation with customization for uppercase, lowercase, numbers, and symbols.
- Secure password storage with a JSON-based database.
- Password search functionality by application/website.
- CSV export of stored data for easier viewing.

## Technologies Used

- Python 3
- CustomTkinter (GUI framework based on Tkinter)
- Pandas (for CSV export)
- PIL (Python Imaging Library for image processing)
- Pyperclip (for copying generated passwords to clipboard)

## Installation

Before running the application, ensure you have the necessary dependencies installed. You can use `pip` to install the required packages.

```bash
# Clone the repository
git clone <repository_url>

# Change to the repository directory
cd <repository_directory>

# Install required packages
pip install -r requirements.txt
