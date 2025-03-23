# Imports
import sys
sys.path.append("C:\\dev\\test")  # Add the test folder to the module search path   # Add the test folder to the module search path
from text_injector import inject_text
import tkinter as tk
from tkinter import scrolledtext
from modules.dictionaries import word_recognition, suggest_word
from modules.file_manager import scan_test_folder

# UI Setup
def launch_ui():
    """
    Launches the UI interface for CodeBot.
    """
    root.mainloop()  # Start the tkinter UI

# Input Handling
conversation_log_path = "C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"

def handle_input(event=None):
    """
    Handles user input, processes CodeBot's response, appends both to the chat history,
    and dynamically backs up interactions into the conversation log.
    """
    from modules.knowledge_base import save_conversation_to_log, retrieve_python_concept

    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field
    output_area.insert(tk.END, f"You: {user_text}\n")

    # Generate response based on user input
    if user_text in ["hello", "hi", "hey", "greetings"]:
        response = "CodeBot: Hello, I'm CodeBot!"
    elif user_text in ["quit"]:
        response = "CodeBot: Goodbye!"
        root.quit()
    elif user_text.startswith("explain"):
        concept = user_text.replace("explain", "").strip()
        response = retrieve_python_concept(concept)
    else:
        response = "CodeBot: I didn't recognize your input."

    # Append CodeBot's response to the chat history
    output_area.insert(tk.END, response + "\n")

    # Backup the interaction
    conversation = f"You: {user_text}\n{response}\n"
    save_conversation_to_log(conversation, log_path=conversation_log_path)

# UI Setup
    """
    Handles user input, processes CodeBot's response, and appends both to the chat history.
    """
    from modules.knowledge_base import retrieve_python_concept
    from modules.text_injector import inject_text


    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field

    # Append user input to the chat history
    output_area.insert(tk.END, f"You: {user_text}\n")

    # Generate CodeBot's response
    if user_text in ["hello", "hi", "hey", "greetings"]:
        response = "CodeBot: Hello, I'm CodeBot!"
    elif user_text in ["quit"]:
        response = "CodeBot: Goodbye!"
        root.quit()  # Close the UI window
    elif user_text.startswith("explain"):
        concept = user_text.replace("explain", "").strip()
        response = retrieve_python_concept(concept)
    elif user_text.startswith("inject knowledge"):
        parts = user_text.replace("inject knowledge", "").strip().split(";")
        file_path = parts[0].strip() if len(parts) > 0 else None
        text = parts[1].strip() if len(parts) > 1 else None
        if file_path and text:
            inject_text(file_path, text, "append")
            response = f"Injected knowledge into {file_path}."
        else:
            response = "CodeBot: Invalid injection command."
    elif user_text.endswith("?"):
        response = "CodeBot: That's an interesting question. Let me think about it!"
    else:
        recognized = word_recognition(user_text)
        if recognized:
            response = f"CodeBot: I recognized these words: {', '.join(recognized)}"
            suggestions = suggest_word(list(recognized)[0])
            if suggestions:
                response += f"\nCodeBot: Here are some word suggestions: {', '.join(suggestions)}"
        else:
            response = "CodeBot: I didn't recognize any valid words. Try again!"

    # Append CodeBot's response to the chat history
    output_area.insert(tk.END, response + "\n")

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
root.mainloop()

# CodeBot_Tracking
