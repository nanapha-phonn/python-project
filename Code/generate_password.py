import tkinter as tk
from tkinter import messagebox
import random
import string


# GUI Window

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x250")


# Password Generator Function

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except:
        messagebox.showwarning("Warning", "Enter a valid positive number for length!")
        return

    all_chars = ""
    if var_lower.get():
        all_chars += string.ascii_lowercase
    if var_upper.get():
        all_chars += string.ascii_uppercase
    if var_digits.get():
        all_chars += string.digits
    if var_symbols.get():
        all_chars += string.punctuation

    if not all_chars:
        messagebox.showwarning("Warning", "Select at least one character type!")
        return

    password = "".join(random.choice(all_chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# Copy to Clipboard Function

def copy_password():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


# GUI Layout

title = tk.Label(root, text="Password Generator", font=("Arial", 18))
title.pack(pady=10)

# Password display
password_entry = tk.Entry(root, font=("Arial", 14), width=30)
password_entry.pack(pady=5)

# Length input
length_label = tk.Label(root, text="Password Length:")
length_label.pack()
length_entry = tk.Entry(root)
length_entry.pack(pady=2)
length_entry.insert(0, "12")  # default length

# Character type checkboxes
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Lowercase", variable=var_lower).pack(anchor='w')
tk.Checkbutton(root, text="Uppercase", variable=var_upper).pack(anchor='w')
tk.Checkbutton(root, text="Digits", variable=var_digits).pack(anchor='w')
tk.Checkbutton(root, text="Symbols", variable=var_symbols).pack(anchor='w')

# Buttons
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=5)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_password)
copy_button.pack(pady=2)

# Run GUI
root.mainloop()
