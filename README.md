# Telegram Message Forwarder

A Python script to forward messages from a Direct Message/Channel/Group to another using the Telethon library. This script also includes a feature to list all your Telegram chats and save their IDs for easy reference.

## Features

- Chat List Generation: Retrieve and save a list of all your Telegram chats (groups, channels, and private chats) along with their IDs.
- Message Forwarding: Forward messages from a source chat to a target chat.
- Resume Support: Automatically resumes forwarding from the last forwarded message ID, even if the script is interrupted.
- Error Logging: Logs errors to a file for debugging.
- Rate Limit Handling: Automatically handles Telegram's rate limits and waits for the required cooldown period.
- Forwarding Speed: Adjustable forwarding speed time (recommended to leave it on 2 seconds per message by default).

## Prerequisites

Before running the script, ensure you have the following:

1. Python 3.7 or higher installed on your system.
2. A Telegram API ID and API Hash. You can obtain these by creating an app on [my.telegram.org](https://my.telegram.org).
3. The Telethon library installed. You can install it using pip:

   ```bash
   pip install telethon

## Steps to Run
Open CMD on your PC and copy-paste the steps bellow
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/sra0sha/Telegram_Message_Forwarder.git
2. Navigate to the project directory:
   ```bash
   cd Telegram_Message_Forwarder
3. Run the script:
   ```bash
   python Telegram_Message_Forwarder.py
