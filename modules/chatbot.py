def process_chat_command(user_input):
    """
    Handles user commands for the chatbot routine and returns appropriate responses.
    """
    user_text = user_input.strip().lower()

    if not user_text:
        return "CodeBot: Please enter a command."
    elif user_text in ["hello", "hi", "hey", "greetings"]:
        return "CodeBot: Hello, I'm CodeBot!"
    elif user_text.startswith("explain"):
        return "CodeBot: This is a command to explain something, but the specific logic is missing."
    elif user_text in ["quit", "exit"]:
        return "CodeBot: Goodbye!"
    else:
        return "CodeBot: I didn't understand that command."
