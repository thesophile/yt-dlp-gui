import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import threading

def download_video():
    video_url = url_entry.get()
    quality = quality_var.get()
    output_format = format_var.get()
    download_folder = folder_var.get()

    if not video_url:
        messagebox.showerror("Input Error", "Please enter the YouTube URL.")
        return

    if not download_folder:
        messagebox.showerror("Input Error", "Please select a download location.")
        return

    # Ensure the folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Path to your virtual environment's Python interpreter
    venv_python = os.path.join("myenv", "bin", "python")

    # yt-dlp command to be executed in the virtual environment
    command = [
        venv_python, '-m', 'yt_dlp',
        '-f', f'bestvideo[height={quality}]+bestaudio',
        '--merge-output-format', output_format,
        '-o', os.path.join(download_folder, '%(title)s.%(ext)s'),
        video_url
    ]

    def run_download():
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                if "ETA" in line:
                    update_progress(line)
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Success", "Download completed successfully!")
            else:
                messagebox.showerror("Error", "An error occurred during download.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Run download in a separate thread to prevent freezing the GUI
    threading.Thread(target=run_download).start()

def update_progress(progress_info):
    progress_label.config(text=progress_info)

def select_folder():
    folder_selected = filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads/videos"))
    if folder_selected:
        folder_var.set(folder_selected)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# YouTube URL label and entry
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Quality options
quality_label = tk.Label(root, text="Select Quality:")
quality_label.pack(pady=5)
quality_var = tk.StringVar(value="720")  # Default value
quality_options = ["360", "480", "720", "1080"]
quality_menu = tk.OptionMenu(root, quality_var, *quality_options)
quality_menu.pack(pady=5)

# Format options
format_label = tk.Label(root, text="Select Output Format:")
format_label.pack(pady=5)
format_var = tk.StringVar(value="mkv")  # Default value
format_options = ["mkv", "mp4", "webm"]
format_menu = tk.OptionMenu(root, format_var, *format_options)
format_menu.pack(pady=5)

# Folder selection
folder_label = tk.Label(root, text="Select Download Folder:")
folder_label.pack(pady=5)
folder_var = tk.StringVar(value=os.path.expanduser("~/Downloads/videos"))  # Default folder
folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Browse", command=select_folder)
folder_button.pack(pady=5)

# Progress label
progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=20)

# Start the main GUI loop
root.mainloop()
