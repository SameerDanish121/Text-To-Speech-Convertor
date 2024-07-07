import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from gtts import gTTS, lang
import os
import shutil
from docx import Document

class TextToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")
        self.root.configure(bg="#f0f0f0")

     
        header_label = tk.Label(root, text="Text to Audio Converter", font=("Arial", 16, "bold"), bg="#333", fg="#fff", padx=10, pady=10)
        header_label.grid(row=0, column=0, columnspan=2, sticky="ew")

      
        self.text_area = tk.Text(root, wrap=tk.WORD, height=10, font=("Arial", 12), bg="#ffffff", fg="#000000", padx=10, pady=10)
        self.text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        self.load_file_button = tk.Button(root, text="Load Text File", command=self.load_file, bg="#4CAF50", fg="#ffffff", font=("Arial", 10))
        self.load_file_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

     
        self.language_combobox = ttk.Combobox(root, font=("Arial", 10))
        self.populate_language_combobox()
        self.language_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

      
        self.convert_button = tk.Button(root, text="Convert to Audio", command=self.convert_text_to_audio, bg="#008CBA", fg="#ffffff", font=("Arial", 10))
        self.convert_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

      
        self.save_button = tk.Button(root, text="Save Audio File", command=self.save_audio_file, bg="#f44336", fg="#ffffff", font=("Arial", 10))
        self.save_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

     
        self.play_button = tk.Button(root, text="Play Audio", command=self.play_audio, bg="#FFC107", fg="#000000", font=("Arial", 10))
        self.play_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

       
        self.status_label = tk.Label(root, text="", bg="#f0f0f0", fg="#000000", font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

     
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def populate_language_combobox(self):
        supported_languages = lang.tts_langs()
        languages = [(name, language) for language, name in supported_languages.items()]
        self.language_combobox['values'] = [name for name, _ in languages]
        self.language_combobox.set("English") 
        self.languages = {name: language for name, language in languages}

    def load_file(self):
      file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.doc;*.docx"), ("All Files", "*.*")])
      if file_path:
        file_content = ""
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        elif file_path.endswith('.doc') or file_path.endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                file_content += para.text + '\n'
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, file_content)
        self.status_label.config(text="File Loaded Successfully")

    def convert_text_to_audio(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            language_name = self.language_combobox.get()
            language_code = self.languages.get(language_name, 'en') 
            tts = gTTS(text, lang=language_code)
            tts.save('output.mp3')
            self.status_label.config(text="Conversion Done! Audio saved as 'output.mp3'.")
        else:
            self.status_label.config(text="Please enter some text.")

    def save_audio_file(self):
        if os.path.exists('output.mp3'):
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
            if file_path:
                shutil.move('output.mp3', file_path)
                self.status_label.config(text=f"File saved as {file_path}")
        else:
            self.status_label.config(text="No audio file found. Please convert text to audio first.")

    def play_audio(self):
        if os.path.exists('output.mp3'):
            os.system('start output.mp3') 
        else:
            self.status_label.config(text="No audio file found. Please convert text to audio first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToAudioApp(root)
    root.mainloop()
 