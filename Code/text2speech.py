# install: pip install pyttsx3 

import tkinter as Tk()
from tkinter import *
import pyttsx3

engine=pytttsx3.init()
def speaknow():
    engine.say(text.get())
    engine.runAndAait()
    engine.stop()

root = Tk()

textv=stringVar()

obj = LabelFrame(root, text = "Text to speech", font = 20, bd = 1)
obj.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

lbl = Label(obj, text = "Text", font = 30)
lbl.pack(side = tk.LEFT, padx = 5)

text = Entry(obj, textvariable = textv, font = 30, width = 25, bd = 5)
text.pack(side = tk, LEFT, padx = 10)

btn = Button(obj, text = "Speak", font=20,bg="black",fg="white",command=speaknow)
btn.pack(side=tk.LEFT,padx=10)

root.titile("Text to speech")
root.geometry("400x200")
root.resizable(False,False)

root.mainloop()
