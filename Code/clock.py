import tkinter as tk
from tkinter import messagebox
import time
import threading


# GUI Window

root = tk.Tk()
root.title("Alarm Clock & Timer")
root.geometry("400x350")


# Live Clock Display

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

clock_label = tk.Label(root, text="", font=("Arial", 24))
clock_label.pack(pady=10)
update_clock()


# Alarm Function

def set_alarm():
    alarm_time = alarm_entry.get()
    if not alarm_time:
        messagebox.showwarning("Warning", "Please enter alarm time!")
        return

    def alarm_thread():
        while True:
            current_time = time.strftime("%H:%M:%S")
            if current_time == alarm_time:
                messagebox.showinfo("Alarm", f"Wake up! {alarm_time} reached!")
                break
            time.sleep(1)

    threading.Thread(target=alarm_thread, daemon=True).start()
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

# Timer Function

def start_timer():
    sec = timer_entry.get()
    if not sec.isdigit():
        messagebox.showwarning("Warning", "Enter timer in seconds!")
        return
    sec = int(sec)

    def countdown(seconds):
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer_label.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            seconds -= 1
        timer_label.config(text="00:00")
        messagebox.showinfo("Timer", "Time's up!")

    threading.Thread(target=countdown, args=(sec,), daemon=True).start()

# GUI Layout

title = tk.Label(root, text="Alarm Clock & Timer", font=("Arial", 18))
title.pack(pady=5)

# Alarm Section
alarm_label = tk.Label(root, text="Set Alarm (HH:MM:SS):")
alarm_label.pack()
alarm_entry = tk.Entry(root)
alarm_entry.pack(pady=2)
alarm_button = tk.Button(root, text="Set Alarm", command=set_alarm)
alarm_button.pack(pady=5)

# Timer Section
timer_label_title = tk.Label(root, text="Set Timer (seconds):")
timer_label_title.pack()
timer_entry = tk.Entry(root)
timer_entry.pack(pady=2)
timer_button = tk.Button(root, text="Start Timer", command=start_timer)
timer_button.pack(pady=5)
timer_label = tk.Label(root, text="00:00", font=("Arial", 20))
timer_label.pack(pady=10)

# Run GUI
root.mainloop()
