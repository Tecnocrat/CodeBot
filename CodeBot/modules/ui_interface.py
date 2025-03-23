import tkinter as tk
from tkinter import scrolledtext
from modules.dictionaries import word_recognition, suggest_word

def launch_ui():
    """
    Launches the UI interface for CodeBot.
    """
    root.mainloop()  # Start the tkinter UI

def handle_input(event=None):
    """
    Handles user input, processes CodeBot's response, and appends both to the chat history.
    """
    user_text = user_entry.get().strip().lower()
    user_entry.delete(0, tk.END)  # Clear the input field

    # Append user input (collapsed if too long)
    if len(user_text) > 50:
        output_area.insert(tk.END, f"You: {user_text[:50]}... [full input hidden]\n")
    else:
        output_area.insert(tk.END, f"You: {user_text}\n")


    # Generate CodeBot's response
    if user_text in ["hello", "hi", "hey", "greetings"]:
        response = "CodeBot: Hello, I'm CodeBot!"
    elif user_text in ["quit"]:
        response = "CodeBot: Goodbye!"
        root.quit()  # Close the UI window
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
