import tkinter as tk
# create main application window
window = tk.Tk() # Sets the window title
window.title("Hello world!") # set the window size ( width x height)
window.geometry("300x150") 
# create a window label widget with the text
label = tk.Label(window, text="Hello world!", font = ("Arial", 16))
label.pack(pady=50)
# start the tkinter eventloop
window.mainloop()
