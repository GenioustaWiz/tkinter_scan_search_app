import os 
import time
import glob
import json
import threading
import tkinter as tk
from tkinter import ttk
# Define the file extensions to scan for
media_exts = ['*.mp3', '*.mp4', '*.avi', '*.mkv', '*.jpg', '*.jpeg', '*.png']
doc_exts = ['*.txt', '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx']

# Define the system folders to exclude from the scan and search
exclude_folders = ['Windows', '$RECYCLE.BIN', 'System Volume Information', 'Program Files', 'Program Files (x86)', 'AppData', 'Local Settings', 'Temporary Internet Files', 'Intel', 'AMD', 'NVIDIA', 'venv']

# Check if cache file exists and load it
cache_file = 'scan_cache5.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {
            'folders': [],
            'media': [],
            'docs': []
            }

# Define the GUI
root = tk.Tk()
root.title("File Scanner")

# Create the search box and button
search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10)
entry = tk.Entry(search_frame)
entry.pack(side=tk.LEFT, padx=5)
button = tk.Button(search_frame, text="Search")
button.pack(side=tk.LEFT, padx=5)

# Create the results listbox
listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(padx=10, pady=10)

# Create a progress bar
style = ttk.Style(root)
style.theme_use('clam')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, style="red.Horizontal.TProgressbar", maximum=100)
progress_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Define the scanning process
# Define a function to scan for new media files and add to cache
def scan_files():
    # Print the type and value of cache['folders'] before the problematic line
    print(type(cache['folders']))
    print(cache['folders'])
    # Get the set of existing folders in the cache
    existing_folders = set([folder_info['path'] for folder_info in cache['folders']])
# Set up the progress bar
    progress_var.set(0)
    progress_bar.configure(style="red.Horizontal.TProgressbar")

    # Get the set of new folders to scan
    new_folders = set()
    # Count the total number of root directories processed
    total_roots = 0
    estimated_total_roots = 1000
    for root, dirs, files in os.walk('/', topdown=True):
        print("Scanning root:", root)  # Add this line to print the current root
        
        # Exclude system folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for dir in dirs:
            if not os.path.join(root, dir) in existing_folders:
                new_folders.add(os.path.join(root, dir))
       # Update the progress bar
        total_roots += 1
        progress_value = (total_roots / estimated_total_roots) * 100
        progress_var.set(progress_value % 100)  # Reset to 0% when reaching 100%
        progress_bar.update_idletasks()  # Update the progress bar
        
        # time.sleep(0.1)

    # Scan each new folder for media and documents
    for folder_path in new_folders:
        media_files = []
        doc_files = []
        for root, dirs, files in os.walk(folder_path):
            # Check if the root directory is a valid integer
            print( "am in the scanning code")
            try:
                int(root.split(os.sep)[-1])
            except ValueError:
                continue
            for file in files:
                if any(file.lower().endswith(ext) for ext in media_exts):
                    media_files.append(os.path.join(root, file))
                    print('Media file',media_files )
                elif any(file.lower().endswith(ext) for ext in doc_exts):
                    doc_files.append(os.path.join(root, file))
                    print('Document file:', doc_files )
                print(f"New folder found: {os.path.join(root, file)}")
                # Update the progress bar
                progress_var.set((int(root.split(os.sep)[-1]) / 255) * 100)
        # Add new folder info and files to cache
        # Create a dictionary for the new folder and add it to cache['folders']
        new_folder_info = {'path': folder_path, 'media': media_files, 'docs': doc_files}
        cache['folders'].append(new_folder_info)
        # cache['folders'].append({'path': folder_path, 'media': media_files, 'docs': doc_files})
        cache['media'].extend(media_files)
        cache['docs'].extend(doc_files)

    # Check existing folders for deleted media and documents
    for folder_info in cache['folders']:
        if not os.path.exists(folder_info['path']):
            # Folder no longer exists, remove it and its files from cache
            cache['folders'].remove(folder_info)
            cache['media'] = [f for f in cache['media'] if f not in folder_info['media']]
            cache['docs'] = [f for f in cache['docs'] if f not in folder_info['docs']]

        else:
            # Folder exists, check for deleted media and documents
            deleted_media = [f for f in folder_info['media'] if not os.path.exists(f)]
            deleted_docs = [f for f in folder_info['docs'] if not os.path.exists(f)]

            if deleted_media or deleted_docs:
                # Files have been deleted, remove them from cache
                for f in deleted_media:
                    cache['media'].remove(f)
                    folder_info['media'].remove(f)
                for f in deleted_docs:
                    cache['docs'].remove(f)
                    folder_info['docs'].remove(f)
    # Update the progress bar style
    progress_bar.configure(style="green.Horizontal.TProgressbar")

    # Save the updated cache to disk
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

# Start the scanning process in a separate thread
def start_scan():
    thread = threading.Thread(target=scan_files)
    thread.start()

# Define a function to search the cached file and folder names
def search_files(query):
    results = []
    # for file in cache['media'] + cache['docs']:
    #     if query.lower() in os.path.basename(file).lower() and not any(exclude_folder in os.path.dirname(file) for exclude_folder in exclude_folders):
    #         file_type = os.path.splitext(file)[1][1:].upper()
    #         results.append(f"{os.path.basename(file)} ({file_type})")
    for folder_info in cache['folders']:
        folder_path = folder_info['path']
        if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
            results.append(f"{os.path.basename(folder_path)} (Folder)")
        
        if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
            file_type = os.path.splitext(folder_path)[1][1:].upper()
            results.append(f"{os.path.basename(folder_path)} ({file_type})")
    return results

# Define a function to update the search results in the GUI
def update_results():
    query = entry.get()
    results = search_files(query)
    listbox.delete(0, tk.END)
    for result in results:
        listbox.insert(tk.END, result.split("/")[-1])

# Define a function to start the auto scan
def start_auto_scan():
    # scan_files()
    start_scan()
    root.after(60000, start_auto_scan) # Reschedule after 1 minute

# Bind the  button to their functions
button.config(command=update_results)

# Start the scanning process automatically
start_scan()

# Start the GUI event loop
root.mainloop()