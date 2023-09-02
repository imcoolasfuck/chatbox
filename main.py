import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, simpledialog, messagebox
from datetime import datetime

# Function to register a new user
def register():
    global username, send_button  # Declare send_button as a global variable
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    # Check if the username already exists
    with open("details.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":")
            if username == stored_username:
                messagebox.showerror("Error", "Username already exists.")
                return

    # Add the new user to the details file
    with open("details.txt", "a") as file:
        file.write(f"{username}:{password}\n")

    username_label.config(text=f"Username: {username}")
    entry.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)
    set_username_button.config(state=tk.DISABLED)
    login_frame.destroy()

# Function to log in an existing user
def login():
    global username, send_button  # Declare send_button as a global variable
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    # Check if the username and password match
    with open("details.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and password == stored_password:
                username_label.config(text=f"Username: {username}")
                entry.config(state=tk.NORMAL)
                send_button.config(state=tk.NORMAL)
                set_username_button.config(state=tk.DISABLED)
                login_frame.destroy()
                return

    messagebox.showerror("Error", "Invalid username or password.")

# Function to send a message when the "Send" button is clicked or Enter key is pressed
def send_message(event=None):
    message = entry.get()
    if message:
        current_time = datetime.now().strftime("%H:%M:%S")  # Get current time
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"{current_time} - {username}: {message}\n")
        chat_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        save_chat_history()

# Function to clear the chat log
def clear_chat():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    chat_log.config(state=tk.DISABLED)
    save_chat_history()

# Function to save chat history to a text file
def save_chat_history():
    with open("chat_history.txt", "w") as file:
        chat_history = chat_log.get(1.0, tk.END)
        file.write(chat_history)

# Function to load chat history from a text file
def load_chat_history(chat_log_widget):
    try:
        with open("chat_history.txt", "r") as file:
            chat_history = file.read()
            chat_log_widget.config(state=tk.NORMAL)
            chat_log_widget.delete(1.0, tk.END)
            chat_log_widget.insert(tk.END, chat_history)
            chat_log_widget.config(state=tk.DISABLED)
    except FileNotFoundError:
        pass

# Create the main window with a size of 1080x720
root = tk.Tk()
root.geometry("1080x720")
root.title("Modern Chatbox")

# Create a label to display the username
username_label = tk.Label(root, text="Username: Not Set", font=("Helvetica", 12, "bold"))
username_label.pack(pady=10)

# Create a text widget to display the chat messages with a modern appearance
chat_log = Text(root, state=tk.DISABLED, wrap=tk.WORD, height=20, width=50, bg="#f2f2f2", fg="#333333",
                font=("Helvetica", 12))
chat_log.pack(expand=True, fill="both", padx=10, pady=5)

# Create a scrollbar for the chat log
scrollbar = Scrollbar(chat_log)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the chat log
chat_log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_log.yview)

# Create an entry widget for typing messages with a modern appearance
entry = Entry(root, state=tk.DISABLED, font=("Helvetica", 12))
entry.pack(fill="both", padx=10, pady=10)

# Create a "Register/Login" button to open the registration/login window
set_username_button = Button(root, text="Register/Login", command=lambda: create_login_window(), font=("Helvetica", 12))
set_username_button.pack()

# Function to create a login window
def create_login_window():
    global login_frame, username_entry, password_entry, send_button
    login_frame = tk.Toplevel(root)
    login_frame.title("Register/Login")
    username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 12))
    username_label.pack()
    username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
    username_entry.pack()
    password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12))
    password_label.pack()
    password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
    password_entry.pack()
    register_button = tk.Button(login_frame, text="Register", command=register, font=("Helvetica", 12))
    register_button.pack()
    login_button = tk.Button(login_frame, text="Login", command=login, font=("Helvetica", 12))
    login_button.pack()

# Load chat history when the application starts
load_chat_history(chat_log)

# Bind the "Enter" key to the send_message function
entry.bind("<Return>", send_message)

# Start the GUI main loop
root.mainloop()
