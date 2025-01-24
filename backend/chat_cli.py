import requests


def chat_with_bot(base_url: str = "http://localhost:8000"):
    """Simple CLI interface for chatting with the course bot"""
    chat_history = []

    print("Welcome to Course Assistant! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Check for exit command
        if user_input.lower() in ["quit", "exit"]:
            print("\nGoodbye!")
            break

        try:
            # Prepare the request
            chat_data = {"question": user_input, "chat_history": chat_history}

            # Make API call
            response = requests.post(f"{base_url}/chat", json=chat_data)

            # Check if request was successful
            response.raise_for_status()

            # Get response data
            data = response.json()
            assistant_response = data["response"]

            # Update chat history
            chat_history.append({"user": user_input, "assistant": assistant_response})

            # Print assistant response
            print("\nAssistant:", assistant_response)
            print("-" * 50)

        except requests.exceptions.RequestException as e:
            print(
                f"\nError: Could not connect to the server. Make sure it's running at {base_url}"
            )
            print(f"Details: {str(e)}")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    chat_with_bot()
