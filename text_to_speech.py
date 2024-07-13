import tkinter as tk
from tkinter import ttk, filedialog
import pyttsx3
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Converter")
        self.engine = pyttsx3.init()

        # Text input
        self.text_label = tk.Label(root, text="Enter Text:")
        self.text_label.pack()
        self.text_entry = tk.Text(root, height=10, width=50)
        self.text_entry.pack()

        # Voice selection
        self.voice_label = tk.Label(root, text="Select Voice:")
        self.voice_label.pack()
        self.voice_combobox = ttk.Combobox(root)
        self.voice_combobox.pack()
        self.populate_voices()

        # Rate adjustment
        self.rate_label = tk.Label(root, text="Speech Rate:")
        self.rate_label.pack()
        self.rate_scale = tk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL)
        self.rate_scale.set(200)
        self.rate_scale.pack()

        # Volume adjustment
        self.volume_label = tk.Label(root, text="Volume:")
        self.volume_label.pack()
        self.volume_scale = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.volume_scale.set(1.0)
        self.volume_scale.pack()

        # Playback controls
        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()
        self.pause_button = tk.Button(root, text="Pause", command=self.pause)
        self.pause_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()

        # Save button
        self.save_button = tk.Button(root, text="Save as Audio", command=self.save_audio)
        self.save_button.pack()

        # Variables to manage playback state
        self.is_paused = False
        self.is_playing = False

    def populate_voices(self):
        voices = self.engine.getProperty('voices')
        self.voice_combobox['values'] = [voice.name for voice in voices]
        self.voice_combobox.current(0)

    def play(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            tk.messagebox.showerror("Error", "Text input is empty!")
            return

        if not self.is_playing or self.is_paused:
            self.engine.setProperty('rate', self.rate_scale.get())
            self.engine.setProperty('volume', self.volume_scale.get())
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[self.voice_combobox.current()].id)
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_playing = True
            self.is_paused = False

    def pause(self):
        if self.is_playing:
            self.engine.stop()
            self.is_paused = True

    def stop(self):
        if self.is_playing:
            self.engine.stop()
            self.is_playing = False
            self.is_paused = False

    def save_audio(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            tk.messagebox.showerror("Error", "Text input is empty!")
            return
        
        self.engine.setProperty('rate', self.rate_scale.get())
        self.engine.setProperty('volume', self.volume_scale.get())
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_combobox.current()].id)
        
        filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
        if filename:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            tk.messagebox.showinfo("Success", f"Audio saved successfully as {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
