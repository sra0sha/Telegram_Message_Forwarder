# Telegram Message Forwarder

A Python script designed to list chat IDs and forward entire direct messages, channels, and more.

## Features
- Get a list of all your chats and their IDs.
- Forward messages from a source chat to a target chat.
- Automatically resume forwarding from the last forwarded message.
- Error handler to not get limited.
- Adjustable forwarding speed time.

## Requirements
- Python 3.7+
- Telethon library (`pip install telethon`)

## Usage
1. Install the required libraries:
   ```bash
   pip install telethon
