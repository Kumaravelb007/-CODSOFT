import tkinter as tk
from tkinter import messagebox
import random
import string

# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("500x600")
window.resizable(False, False)
window.configure(bg="#34495e")

# Title label
title_label = tk.Label(
    window,
    text="🔐 Password Generator",
    font=("Arial", 24, "bold"),
    bg="#34495e",
    fg="#ecf0f1"
)
title_label.pack(pady=20)

# Frame for password length
length_frame = tk.Frame(window, bg="#34495e")
length_frame.pack(pady=10)

length_label = tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 14),
    bg="#34495e",
    fg="#ecf0f1"
)
length_label.pack(side=tk.LEFT, padx=10)

# Entry for password length
length_entry = tk.Entry(
    length_frame,
    font=("Arial", 14),
    width=10,
    justify="center",
    borderwidth=3,
    relief="ridge"
)
length_entry.pack(side=tk.LEFT, padx=10)
length_entry.insert(0, "12")  # Default length

# Frame for complexity options
complexity_frame = tk.LabelFrame(
    window,
    text="Password Complexity",
    font=("Arial", 12, "bold"),
    bg="#34495e",
    fg="#ecf0f1",
    padx=20,
    pady=15
)
complexity_frame.pack(pady=20)

# Variables for checkboxes
include_lowercase = tk.BooleanVar(value=True)
include_uppercase = tk.BooleanVar(value=True)
include_numbers = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=True)

# Checkboxes for character types
tk.Checkbutton(
    complexity_frame,
    text="Include Lowercase (a-z)",
    variable=include_lowercase,
    font=("Arial", 12),
    bg="#34495e",
    fg="#ecf0f1",
    selectcolor="#2c3e50",
    activebackground="#34495e",
    activeforeground="#ecf0f1"
).pack(anchor="w", pady=5)

tk.Checkbutton(
    complexity_frame,
    text="Include Uppercase (A-Z)",
    variable=include_uppercase,
    font=("Arial", 12),
    bg="#34495e",
    fg="#ecf0f1",
    selectcolor="#2c3e50",
    activebackground="#34495e",
    activeforeground="#ecf0f1"
).pack(anchor="w", pady=5)

tk.Checkbutton(
    complexity_frame,
    text="Include Numbers (0-9)",
    variable=include_numbers,
    font=("Arial", 12),
    bg="#34495e",
    fg="#ecf0f1",
    selectcolor="#2c3e50",
    activebackground="#34495e",
    activeforeground="#ecf0f1"
).pack(anchor="w", pady=5)

tk.Checkbutton(
    complexity_frame,
    text="Include Symbols (!@#$%^&*)",
    variable=include_symbols,
    font=("Arial", 12),
    bg="#34495e",
    fg="#ecf0f1",
    selectcolor="#2c3e50",
    activebackground="#34495e",
    activeforeground="#ecf0f1"
).pack(anchor="w", pady=5)

# Function to generate the password
def generate_password():
    try:
        # Get the desired length
        length = int(length_entry.get())
        
        # Make sure the length is reasonable
        if length < 4:
            messagebox.showwarning("Warning", "Password length should be at least 4 characters!")
            return
        
        if length > 100:
            messagebox.showwarning("Warning", "Password length should not exceed 100 characters!")
            return
        
        # Build the character pool based on selected options
        characters = ""
        
        if include_lowercase.get():
            characters += string.ascii_lowercase  # a-z
        
        if include_uppercase.get():
            characters += string.ascii_uppercase  # A-Z
        
        if include_numbers.get():
            characters += string.digits  # 0-9
        
        if include_symbols.get():
            characters += string.punctuation  # !@#$%^&*()_+
        
        # Make sure at least one option is selected
        if not characters:
            messagebox.showwarning("Warning", "Please select at least one character type!")
            return
        
        # Generate the password by randomly picking characters
        password = ""
        for i in range(length):
            password += random.choice(characters)
        
        # Display the password
        password_display.config(state="normal")  # Enable editing temporarily
        password_display.delete(0, tk.END)  # Clear any old password
        password_display.insert(0, password)  # Insert new password
        password_display.config(state="readonly")  # Make it read-only again
        
        # Show strength indicator
        strength = calculate_strength(password)
        strength_label.config(text=f"Password Strength: {strength}")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length!")

# Function to calculate password strength (simple version)
def calculate_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    # Count how many types are included
    types_count = sum([has_lower, has_upper, has_digit, has_symbol])
    
    # Simple strength calculation
    if length < 8 or types_count < 2:
        return "Weak 😟"
    elif length < 12 or types_count < 3:
        return "Medium 😐"
    else:
        return "Strong 💪"

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_display.get()
    if password:
        window.clipboard_clear()
        window.clipboard_append(password)
        messagebox.showinfo("Success", "Password copied to clipboard! ✓")
    else:
        messagebox.showwarning("Warning", "No password to copy!")

# Generate button
generate_button = tk.Button(
    window,
    text="🔑 Generate Password",
    font=("Arial", 14, "bold"),
    bg="#27ae60",
    fg="white",
    command=generate_password,
    padx=20,
    pady=10,
    borderwidth=3,
    relief="raised",
    cursor="hand2"
)
generate_button.pack(pady=20)

# Frame for password display
display_frame = tk.Frame(window, bg="#34495e")
display_frame.pack(pady=10)

# Entry to display the generated password
password_display = tk.Entry(
    display_frame,
    font=("Courier", 14, "bold"),
    width=35,
    justify="center",
    borderwidth=3,
    relief="sunken",
    bg="#ecf0f1",
    fg="#2c3e50",
    state="readonly"
)
password_display.pack(pady=10)

# Copy button
copy_button = tk.Button(
    display_frame,
    text="📋 Copy to Clipboard",
    font=("Arial", 12),
    bg="#3498db",
    fg="white",
    command=copy_to_clipboard,
    padx=15,
    pady=5,
    borderwidth=2,
    relief="raised",
    cursor="hand2"
)
copy_button.pack(pady=5)

# Strength indicator label
strength_label = tk.Label(
    window,
    text="Password Strength: -",
    font=("Arial", 12, "bold"),
    bg="#34495e",
    fg="#f39c12"
)
strength_label.pack(pady=10)

# Footer
footer_label = tk.Label(
    window,
    text="💡 Tip: Use a mix of all character types for the strongest password!",
    font=("Arial", 10, "italic"),
    bg="#34495e",
    fg="#95a5a6"
)
footer_label.pack(side=tk.BOTTOM, pady=20)

# Start the application
window.mainloop()