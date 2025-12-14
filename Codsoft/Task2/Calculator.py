import tkinter as tk
from tkinter import messagebox

# Let's create our main calculator window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("400x500")
window.resizable(False, False)
window.configure(bg="#2c3e50")

# Variables to store our numbers and operation
first_number = None
operation = None
clear_on_next = False

# This will be our display screen
display = tk.Entry(
    window,
    font=("Arial", 24),
    justify="right",
    bg="#ecf0f1",
    fg="#2c3e50",
    borderwidth=5,
    relief="ridge"
)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="ew")
display.insert(0, "0")

# Function to handle number button clicks
def button_click(number):
    global clear_on_next
    
    current = display.get()
    
    # If we just calculated something, clear the display for new input
    if clear_on_next:
        display.delete(0, tk.END)
        clear_on_next = False
        current = ""
    
    # If display shows "0", replace it. Otherwise, append
    if current == "0":
        display.delete(0, tk.END)
        display.insert(0, str(number))
    else:
        display.insert(tk.END, str(number))

# Function to clear everything
def clear():
    global first_number, operation, clear_on_next
    display.delete(0, tk.END)
    display.insert(0, "0")
    first_number = None
    operation = None
    clear_on_next = False

# Function to handle operations (+, -, *, /)
def set_operation(op):
    global first_number, operation, clear_on_next
    
    try:
        # Store the first number
        first_number = float(display.get())
        operation = op
        clear_on_next = True
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# Function to calculate the result
def calculate():
    global first_number, operation, clear_on_next
    
    # Make sure we have everything we need
    if first_number is None or operation is None:
        return
    
    try:
        # Get the second number
        second_number = float(display.get())
        result = None
        
        # Do the math based on the operation
        if operation == "+":
            result = first_number + second_number
        elif operation == "-":
            result = first_number - second_number
        elif operation == "*":
            result = first_number * second_number
        elif operation == "/":
            # Watch out for division by zero!
            if second_number == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                clear()
                return
            result = first_number / second_number
        
        # Show the result
        display.delete(0, tk.END)
        
        # Format the result nicely (remove .0 if it's a whole number)
        if result == int(result):
            display.insert(0, str(int(result)))
        else:
            display.insert(0, str(round(result, 8)))
        
        # Reset for next calculation
        first_number = None
        operation = None
        clear_on_next = True
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# Function to handle decimal point
def add_decimal():
    current = display.get()
    if "." not in current:
        display.insert(tk.END, ".")

# Now let's create all the buttons
# Button styling
button_config = {
    "font": ("Arial", 16, "bold"),
    "width": 5,
    "height": 2,
    "borderwidth": 3,
    "relief": "raised"
}

number_color = "#3498db"  # Blue for numbers
operation_color = "#e74c3c"  # Red for operations
special_color = "#95a5a6"  # Gray for special buttons

# Row 1: Clear and operations
tk.Button(
    window, text="C", command=clear,
    bg=special_color, fg="white", **button_config
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    window, text="/", command=lambda: set_operation("/"),
    bg=operation_color, fg="white", **button_config
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    window, text="*", command=lambda: set_operation("*"),
    bg=operation_color, fg="white", **button_config
).grid(row=1, column=2, padx=5, pady=5)

tk.Button(
    window, text="-", command=lambda: set_operation("-"),
    bg=operation_color, fg="white", **button_config
).grid(row=1, column=3, padx=5, pady=5)

# Row 2: 7, 8, 9
tk.Button(
    window, text="7", command=lambda: button_click(7),
    bg=number_color, fg="white", **button_config
).grid(row=2, column=0, padx=5, pady=5)

tk.Button(
    window, text="8", command=lambda: button_click(8),
    bg=number_color, fg="white", **button_config
).grid(row=2, column=1, padx=5, pady=5)

tk.Button(
    window, text="9", command=lambda: button_click(9),
    bg=number_color, fg="white", **button_config
).grid(row=2, column=2, padx=5, pady=5)

tk.Button(
    window, text="+", command=lambda: set_operation("+"),
    bg=operation_color, fg="white", **button_config
).grid(row=2, column=3, padx=5, pady=5)

# Row 3: 4, 5, 6
tk.Button(
    window, text="4", command=lambda: button_click(4),
    bg=number_color, fg="white", **button_config
).grid(row=3, column=0, padx=5, pady=5)

tk.Button(
    window, text="5", command=lambda: button_click(5),
    bg=number_color, fg="white", **button_config
).grid(row=3, column=1, padx=5, pady=5)

tk.Button(
    window, text="6", command=lambda: button_click(6),
    bg=number_color, fg="white", **button_config
).grid(row=3, column=2, padx=5, pady=5)

# Row 4: 1, 2, 3
tk.Button(
    window, text="1", command=lambda: button_click(1),
    bg=number_color, fg="white", **button_config
).grid(row=4, column=0, padx=5, pady=5)

tk.Button(
    window, text="2", command=lambda: button_click(2),
    bg=number_color, fg="white", **button_config
).grid(row=4, column=1, padx=5, pady=5)

tk.Button(
    window, text="3", command=lambda: button_click(3),
    bg=number_color, fg="white", **button_config
).grid(row=4, column=2, padx=5, pady=5)

# Row 5: 0, decimal, equals
tk.Button(
    window, text="0", command=lambda: button_click(0),
    bg=number_color, fg="white", **button_config
).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

tk.Button(
    window, text=".", command=add_decimal,
    bg=special_color, fg="white", **button_config
).grid(row=5, column=2, padx=5, pady=5)

tk.Button(
    window, text="=", command=calculate,
    bg="#27ae60", fg="white", **button_config  # Green for equals
).grid(row=4, column=3, rowspan=2, padx=5, pady=5, sticky="ns")

# Configure grid weights so buttons expand properly
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

# Start the main event loop
window.mainloop()
