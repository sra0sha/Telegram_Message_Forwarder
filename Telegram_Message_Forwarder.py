from telethon.sync import TelegramClient
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import time
import os
import signal

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# ********* Chat ID *********

print("----- starting the Chat List program -----")
while True:
    WannaList = str(input("Do You Want to Get Your Chat's IDs? yes/no "))
    if WannaList.lower() == "yes":
        api_id = int(input("Enter Your API ID: "))
        api_hash = str(input("Enter Your API Hash: "))

        client = TelegramClient("session_name", api_id, api_hash)

        with client:
            dialogs = client.get_dialogs()
            # Save Chat_List.txt in the script's directory
            chat_list_path = os.path.join(script_directory, "Chat_List.txt")
            with open(chat_list_path, "w", encoding="utf-8") as file:
                for dialog in dialogs:
                    file.write(
                        f"Chat: {dialog.name}\nID: {dialog.id}\nType: {type(dialog.entity).__name__}\n"
                    )
                    file.write("------\n")

        print(f"Chat list has been saved to '{chat_list_path}'.")
        break
    elif WannaList.lower() == "no":
        break


# ********* Message Forwarder *********

print("----- starting the Forwarder program -----")
# Replace these with your own values that you got in Chat_List.txt
# Username or ID of the source chat
source_chat = int(input("Enter Source Chat's ID: "))
# Username or ID of the target chat
target_chat = int(input("Enter Target Chats's ID: "))

# File to store the last forwarded message ID
LAST_FORWARDED_FILE = os.path.join(script_directory, "Last_Forwarded_Message.txt")
print(f"Last_Forwarded_Message.txt will be saved at: {LAST_FORWARDED_FILE}")

# File to store errors
ERROR_LOG_FILE = os.path.join(script_directory, "forward_errors.txt")

# Create a Telegram client
client = TelegramClient("session_name", api_id, api_hash)


# Function to log errors to a file
def log_error(error_message):
    try:
        with open(ERROR_LOG_FILE, "a") as error_file:
            error_file.write(f"{time.ctime()}: {error_message}\n")
    except Exception as e:
        print(f"Failed to log error: {e}")


# Function to save the last forwarded message ID
def save_last_forwarded(message_id):
    try:
        print(
            f"Saving last forwarded message ID: {message_id} to {LAST_FORWARDED_FILE}"
        )
        with open(LAST_FORWARDED_FILE, "w") as file:
            file.write(str(message_id))
    except Exception as e:
        print(f"Failed to save last forwarded message ID: {e}")


# Function to read the last forwarded message ID
def read_last_forwarded():
    if os.path.exists(LAST_FORWARDED_FILE):
        try:
            with open(LAST_FORWARDED_FILE, "r") as file:
                return int(file.read().strip())
        except Exception as e:
            print(f"Failed to read last forwarded message ID: {e}")
    return None


async def forward_messages():
    await client.start()
    print("Client Created. Forwarding messages...")

    # Force create the file at the start of the script (if it doesn't exist)
    if not os.path.exists(LAST_FORWARDED_FILE):
        with open(LAST_FORWARDED_FILE, "w") as file:
            file.write("0")  # Initialize with a dummy ID
        print(f"Created {LAST_FORWARDED_FILE} with dummy ID.")

    # Get the source and target chat entities
    source_entity = await client.get_entity(source_chat)
    target_entity = await client.get_entity(target_chat)

    # Read the last forwarded message ID
    last_forwarded = read_last_forwarded()
    resume_from_id = last_forwarded if last_forwarded is not None else None

    try:
        # Iterate through all messages in the source chat in reverse order (oldest first)
        async for message in client.iter_messages(source_entity, reverse=True):
            # Skip messages that have already been forwarded
            if resume_from_id is not None and message.id <= resume_from_id:
                continue

            while True:
                try:
                    # Forward the message to the target chat
                    await client.forward_messages(target_entity, message)
                    print(f"Forwarded message: {message.id} (Date: {message.date})")
                    # Save the last forwarded message ID
                    save_last_forwarded(message.id)
                    # Add a delay to avoid hitting rate limits
                    await asyncio.sleep(2)
                    break  # Exit the retry loop if forwarding succeeds
                except FloodWaitError as e:
                    # Handle Telegram's cooldown
                    wait_time = e.seconds
                    print(f"Rate limit hit. Waiting for {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    error_message = f"Failed to forward message {message.id}: {e}"
                    log_error(error_message)
                    break  # Exit the retry loop on other errors

    except asyncio.CancelledError:
        print("Forwarding interrupted. Saving progress...")
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        log_error(error_message)
    finally:
        print("Forwarding complete or interrupted. Exiting gracefully.")


# Handle graceful shutdown on SIGINT (Ctrl+C)
def handle_shutdown(signal, frame):
    print("\nShutdown signal received. Exiting gracefully...")
    client.loop.stop()


# Register the signal handler
signal.signal(signal.SIGINT, handle_shutdown)

# Run the script
with client:
    try:
        client.loop.run_until_complete(forward_messages())
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting gracefully.")
