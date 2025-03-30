# Imports
import sys
import tkinter as tk
from tkinter import scrolledtext
from modules.dictionaries import word_recognition, suggest_word
from modules.file_manager import scan_test_folder
from modules.knowledge_base import retrieve_python_concept, save_conversation_to_log, inject_text
from core.ai_engine import explain_python_code
from modules.chatbot import process_chat_command

# Add CodeBot folder to Python search path
sys.path.append("C:\\dev\\CodeBot")

# Global Variables
CONVERSATION_LOG_PATH = "C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"
quit_flag = False  # Global flag to exit the app

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
    global quit_flag

    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field

    if quit_flag:
        root.quit()  # Exit application immediately
        return

    if not user_text:
        response = "CodeBot: Please enter a message."
    elif user_text in ["quit"]:
        quit_flag = True
        response = "CodeBot: Goodbye!"
    elif user_text.startswith("explain python"):
        # Extract the Python code snippet from the input
        code_snippet = user_text.replace("explain python", "").strip()
        if not code_snippet:
            response = "CodeBot: Please provide a Python code snippet to explain."
        else:
            response = explain_python_code(code_snippet)
    else:
        response = "CodeBot: I didn't understand that command."

    # Append user input and response to chat history
    output_area.insert(tk.END, f"You: {user_text}\n{response}\n")

    # Save conversation to log
    save_conversation_to_log(f"You: {user_text}\n{response}", log_path=CONVERSATION_LOG_PATH)

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