import tkinter as tk
import random
# create window
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("400x300")
root.resizable(False, False)

# Game variables 
# set the range for the random number
lower_bound = 1
upper_bound = 100
secret_number = random.randint(lower_bound, upper_bound)
attempts = 5
def check_guess():
    global attempts

    try:
        user_guess = int(entry.get())
        attempts += 1

        if user_guess < secret_number:
            result_label.config(text="Too Low! Try again.")
        elif user_guess > secret_number:
            result_label.config(text="Too High! Try again.")
        else:
            result_label.config(text=f" Correct! You guessed it in {attempts} tries!")
    except ValueError:
        result_label.config(text="Please enter a valid number!")

def restart_game():
    global secret_number, attempts
    secret_number = random.randint(lower_bound, upper_bound)
    attempts = 0
    result_label.config(text="Game restarted! Guess again.")
    entry.delete(0, tk.END)


# Widgets
title_label = tk.Label(root, text="Number Guessing Game", font=("Arial", 16))
title_label.pack(pady=10)

info_label = tk.Label(root, text="Guess a number between 1 and 100")
info_label.pack()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

guess_button = tk.Button(root, text="Guess", command=check_guess)
guess_button.pack(pady=5)

restart_button = tk.Button(root, text="Restart", command=restart_game)
restart_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()
