import tkinter as tk
from tkinter import ttk
import os 
import json

# Define the function that scans for media files and documents
def scan():
    # Get the root folder to scan
    root_folder = "/"

    # Define the list of media file extensions
    media_exts = ['.mp3', '.mp4', '.avi', '.flv', '.mov', '.wmv']

    # Set up the progress bar
    progress_var.set(0)
    progress_bar.configure(style="red.Horizontal.TProgressbar")

    # Scan the root folder for media files and documents
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Check if the file is a media file
            if os.path.splitext(filename)[1] in media_exts:
                # Add the file to the cache
                cache.append(os.path.join(dirpath, filename))
            else:
                # Check if the file is a document
                if filename.endswith(".doc") or filename.endswith(".docx") or filename.endswith(".pdf"):
                    # Add the file to the cache
                    cache.append(os.path.join(dirpath, filename))
        
        # Update the progress bar
        progress_var.set((int(dirpath.split(os.sep)[-1]) / 255) * 100)

    # Update the progress bar style
    progress_bar.configure(style="green.Horizontal.TProgressbar")

# Define the function that starts the scanning process
def start_scan():
    # Call the scan function
    scan()

# Create the GUI
root = tk.Tk()

# Create a progress bar
style = ttk.Style()
style.theme_use('clam')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, style="red.Horizontal.TProgressbar", maximum=100)
progress_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create a button to start the scan
start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.pack()

# Start the GUI
root.mainloop()
