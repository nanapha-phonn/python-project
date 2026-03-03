from tkinter import *
from tkinter import ttk, messagebox
import requests

root = Tk()
root.title("Translator 3.14 Compatible")
root.geometry("800x400")

# Supported languages
languages = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "Khmer": "km"
}

def translate_now():
    try:
        text = text1.get(1.0, END).strip()
        if not text:
            return
        src = languages[combo1.get()]
        dest = languages[combo2.get()]

        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={src}|{dest}"
        response = requests.get(url).json()
        translated_text = response['responseData']['translatedText']

        text2.delete(1.0, END)
        text2.insert(END, translated_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Combo boxes for languages
combo1 = ttk.Combobox(root, values=list(languages.keys()), state="readonly")
combo1.place(x=50, y=20)
combo1.set("English")

combo2 = ttk.Combobox(root, values=list(languages.keys()), state="readonly")
combo2.place(x=550, y=20)
combo2.set("French")

# Text areas
text1 = Text(root, font=("Arial", 14), wrap=WORD)
text1.place(x=50, y=60, width=300, height=200)

text2 = Text(root, font=("Arial", 14), wrap=WORD)
text2.place(x=450, y=60, width=300, height=200)

# Translate button
btn = Button(root, text="Translate", command=translate_now)
btn.place(x=360, y=150)

root.mainloop()
