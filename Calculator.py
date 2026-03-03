import tkinter as tk

# --- Functions ---
def press(value):
    entry_var.set(entry_var.get() + str(value))

def equal():
    try:
        result = str(eval(entry_var.get()))
        entry_var.set(result)
    except:
        entry_var.set("Error")

def clear():
    entry_var.set("")

# --- Main Window ---
root = tk.Tk()
root.title("Professional Calculator")
root.geometry("320x450")
root.resizable(False, False)

# --- Entry Display ---
entry_var = tk.StringVar()
entry = tk.Entry(
    root,
    textvariable=entry_var,
    font=("Arial", 24),
    bd=10,
    relief="ridge",
    justify="right"
)
entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

# --- Buttons Layout ---
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(root, text=text, font=("Arial", 18), command=equal)
    else:
        btn = tk.Button(root, text=text, font=("Arial", 18),
                        command=lambda t=text: press(t))
    btn.grid(row=row, column=col, sticky="nsew")

# Clear Button (Full Width)
clear_btn = tk.Button(root, text="C", font=("Arial", 18),
                      bg="red", fg="white", command=clear)
clear_btn.grid(row=5, column=0, columnspan=4, sticky="nsew")

# --- Make Grid Expand Evenly ---
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# --- Run App ---
root.mainloop()
