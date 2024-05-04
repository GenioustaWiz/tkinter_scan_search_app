import os
import glob
import json
import tkinter as tk

# Define the file extensions to scan for
media_extensions = ['*.mp3', '*.mp4', '*.avi', '*.mkv', '*.jpg', '*.jpeg', '*.png']
doc_extensions = ['*.txt', '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx']

# Define the system folders to exclude from the scan and search
exclude_folders = ['Windows', '$RECYCLE.BIN', 'System Volume Information', 'Program Files', 'Program Files (x86)', 'AppData', 'Local Settings', 'Temporary Internet Files', 'Intel', 'AMD', 'NVIDIA']

# Check if cache file exists and load it
cache_file = 'scan_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {'media': [], 'docs': [], 'folders': []}

# Define a function to scan for new media files and add to cache
def scan_files():
    for root, dirs, files in os.walk('/', topdown=True):
        # Exclude system folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for extension in media_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['media']:
                    file_info = {
                        'path': file,
                        'size': os.path.getsize(file),
                        'type': extension.split('.')[-1].upper()
                    }
                    cache['media'].append(file_info)
                    print(f"New media file found: {file}")
        for extension in doc_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['docs']:
                    file_info = {
                        'path': file,
                        'size': os.path.getsize(file),
                        'type': extension.split('.')[-1].upper()
                    }
                    cache['docs'].append(file_info)
                    print(f"New document found: {file}")
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if folder_path not in cache['folders']:
                folder_info = {
                    'path': folder_path,
                    'size': os.path.getsize(folder_path),
                    'type': 'FOLDER'
                }
                cache['folders'].append(folder_info)
                print(f"New folder found: {folder_path}")
                
    # Save the updated cache file
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

# Define a function to search the cached file and folder names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs']:
        if query.lower() in os.path.basename(file).lower() and not any(exclude_folder in os.path.dirname(file) for exclude_folder in exclude_folders):
            file_type = os.path.splitext(file)[1]
            results.append(os.path.basename(file) + " (" + file_type + ")")
    for folder_info in cache['folders']:
        folder_path = folder_info['path']
        if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
            results.append(os.path.basename(folder_path) + " (Folder)")
    return results

# Define a function to update the search results in the GUI
def update_results():
    query = entry.get()
    results = search_files(query)
    listbox.delete(0, tk.END)
    for result in results:
        listbox.insert(tk.END, result)

# Define a function to start the auto scan
def start_auto_scan():
    scan_files()
    root.after(60000, start_auto_scan) # Reschedule after 1

# Create the GUI
root = tk.Tk()
root.geometry("800x600")

# Create the search box and button
search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10)
entry = tk.Entry(search_frame)
entry.pack(side=tk.LEFT, padx=5)
button = tk.Button(search_frame, text="Search", command=update_results)
button.pack(side=tk.LEFT, padx=5)

# Create the listbox to display search results
listbox = tk.Listbox(root, height=20, width=100)
listbox.pack(padx=10, pady=10)

# Create the Start Scan button
scan_button = tk.Button(root, text="Start Scan", command=scan_files)
scan_button.pack(padx=10, pady=10)

# Create the Auto Scan checkbox
auto_scan_var = tk.BooleanVar()
auto_scan_var.set(True)
auto_scan_checkbox = tk.Checkbutton(root, text="Auto Scan on Start-up", variable=auto_scan_var)
auto_scan_checkbox.pack(padx=10, pady=10)

# Start the auto scan if enabled
if auto_scan_var.get():
    start_auto_scan()

# Start the GUI event loop
root.mainloop()