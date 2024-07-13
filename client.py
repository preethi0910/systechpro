import tkinter as tk
from tkinter import filedialog, messagebox
import requests

SERVER_URL = 'http://127.0.0.1:5000'

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as f:
            response = requests.post(f'{SERVER_URL}/upload', files={'file': f})
        messagebox.showinfo('Info', response.json().get('message'))

def download_file():
    filename = filedialog.askstring('Download File', 'Enter filename:')
    if filename:
        response = requests.get(f'{SERVER_URL}/download/{filename}', stream=True)
        if response.status_code == 200:
            save_path = filedialog.asksaveasfilename(defaultextension=".*", initialfile=filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo('Info', 'File downloaded successfully')
        else:
            messagebox.showerror('Error', 'File not found')

def delete_file():
    filename = filedialog.askstring('Delete File', 'Enter filename:')
    if filename:
        response = requests.delete(f'{SERVER_URL}/delete/{filename}')
        messagebox.showinfo('Info', response.json().get('message'))

def list_files():
    response = requests.get(f'{SERVER_URL}/files')
    files = response.json()
    messagebox.showinfo('Files', '\n'.join(files))

def create_gui():
    root = tk.Tk()
    root.title("File Sharing App")

    upload_btn = tk.Button(root, text="Upload File", command=upload_file)
    upload_btn.pack(pady=5)

    download_btn = tk.Button(root, text="Download File", command=download_file)
    download_btn.pack(pady=5)

    delete_btn = tk.Button(root, text="Delete File", command=delete_file)
    delete_btn.pack(pady=5)

    list_btn = tk.Button(root, text="List Files", command=list_files)
    list_btn.pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
