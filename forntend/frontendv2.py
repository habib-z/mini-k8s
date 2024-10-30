# frontend.py

import os
import requests

# Configuration from environment variables
BACKEND_URL = os.getenv("BACKEND_URL")
API_KEY = os.getenv("API_KEY")

def main():
    print("Simple CLI for sending messages to the backend.")
    while True:
        command = input("Enter 'send' to send a message, 'get' to retrieve messages, or 'exit' to quit: ")
        if command == "send":
            message = input("Enter your message: ")
            response = requests.post(
                f"{BACKEND_URL}/save_message",
                json={"message": message},
                headers={"X-API-KEY": API_KEY}
            )
            print(response.json())
        elif command == "get":
            response = requests.get(f"{BACKEND_URL}/get_messages", headers={"X-API-KEY": API_KEY})
            print(response.json().get("messages", []))
        elif command == "exit":
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
