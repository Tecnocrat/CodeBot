# Imports
import sys
sys.path.append("C:\\dev\\CodeBot")  # Add the CodeBot folder to the Python search path
import tkinter as tk
from tkinter import scrolledtext
from modules.dictionaries import word_recognition, suggest_word
from modules.file_manager import scan_test_folder
from modules.knowledge_base import retrieve_python_concept, save_conversation_to_log
from modules.text_injector import inject_text

# Global Variables
conversation_log_path = "C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"

# UI Setup
def launch_ui():
    """
    Launches the UI interface for CodeBot.
    """
    root.mainloop()  # Start the tkinter UI

# Input Handling
def handle_input(event=None):
    """
    Handles user input, processes CodeBot's response, appends both to the chat history,
    and backs up interactions into the conversation log.
    """
    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field

    # Prevent empty input
    if not user_text:
        response = "CodeBot: Please enter a message."
    elif user_text in ["hello", "hi", "hey", "greetings"]:
        response = "CodeBot: Hello, I'm CodeBot!"
    elif user_text in ["quit"]:
        response = "CodeBot: Goodbye!"
        root.quit()  # Close the UI window
    elif user_text.startswith("explain"):
        # Retrieve a Python concept
        concept = user_text.replace("explain", "").strip()
        response = retrieve_python_concept(concept)
    elif user_text.startswith("inject knowledge"):
        # Inject knowledge into a specified file
        parts = user_text.replace("inject knowledge", "").strip().split(";")
        file_path = parts[0].strip() if len(parts) > 0 else None
        text = parts[1].strip() if len(parts) > 1 else None
        if file_path and text:
            inject_text(file_path, text, "append")
            response = f"CodeBot: Injected knowledge into {file_path}."
        else:
            response = "CodeBot: Invalid injection command."
    elif user_text.endswith("?"):
        # Respond to questions generically
        response = "CodeBot: That's an interesting question. Let me think about it!"
    else:
        # Use word recognition
        recognized = word_recognition(user_text)
        if recognized:
            response = f"CodeBot: I recognized these words: {', '.join(recognized)}"
            suggestions = suggest_word(list(recognized)[0])
            if suggestions:
                response += f"\nCodeBot: Here are some word suggestions: {', '.join(suggestions)}"
        else:
            response = "CodeBot: I didn't recognize any valid words. Try again!"

    # Append user input and response to chat history
    output_area.insert(tk.END, f"You: {user_text}\n{response}\n")

    # Save conversation to log
    conversation = f"You: {user_text}\n{response}\n"
    save_conversation_to_log(conversation, log_path=conversation_log_path)

# Create the main UI window
root = tk.Tk()
root.title("CodeBot Chat")

# Create a scrolled text area for output
output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 12))
output_area.pack(pady=10)

# Create an entry widget for user input
user_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
user_entry.pack(pady=10)
user_entry.bind("<Return>", handle_input)  # Enter key triggers the function

# Create a button to send input
send_button = tk.Button(root, text="Send", command=handle_input, font=("Helvetica", 12))
send_button.pack(pady=10)

# Run the UI loop
launch_ui()

# CodeBot_Tracking
