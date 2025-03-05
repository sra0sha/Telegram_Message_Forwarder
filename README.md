# Telegram Message Forwarder

A Python bot to list Telegram chat IDs and forward entire DM, Channels, and more.

## Features
- Get a list of all your chats and their IDs.
- Forward messages from a source chat to a target chat.
- Automatically resume forwarding from the last forwarded message.
- Error handler to not get limited.
- Adjustable forwarding speed time (recommended to leave it on 2 by default).

## Requirements
- Python 3.7+
- Telethon library (`pip install telethon`)

### Steps to Run
1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/sra0sha/Telegram_Message_Forwarder.git
2. Navigate to the project directory:
   ```bash
   cd Telegram_Message_Forwarder
3. Run the script:
   ```bash
   python Telegram_Message_Forwarder.py
