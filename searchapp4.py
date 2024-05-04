import os 
import glob
import json
import threading
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

# # Create the Start Scan button
# scan_button = tk.Button(root, text="Start Scan")
# scan_button.pack(padx=10, pady=10)

# # Create the Auto Scan checkbox
# auto_scan_var = tk.BooleanVar()
# auto_scan_var.set(True)
# auto_scan_checkbox = tk.Checkbutton(root, text="Auto Scan on Start-up", variable=auto_scan_var)
# auto_scan_checkbox.pack(padx=10, pady=10)

# Define the scanning process
# Define a function to scan for new media files and add to cache
def scan_files():
    for root, dirs, files in os.walk('/', topdown=True):
        # Exclude system folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for extension in media_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['media']:
                    cache['media'].append(file)
                    print(f"New media file found: {file}")
        for extension in doc_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['docs']:
                    cache['docs'].append(file)
                    print(f"New document found: {file}")
        for folder in dirs:
            if folder not in cache['folders']:
                cache['folders'].append(folder)
                print(f"New folder found: {os.path.join(root, folder)}")

    # Save the updated cache file
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
# Start the scanning process in a separate thread
def start_scan():
    thread = threading.Thread(target=scan_files)
    thread.start()

# Define a function to search the cached file and folder names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs']:
        if query.lower() in os.path.basename(file).lower() and not any(exclude_folder in os.path.dirname(file) for exclude_folder in exclude_folders):
            file_type = os.path.splitext(file)[1][1:].upper()
            results.append(f"{os.path.basename(file)} ({file_type})")
    for folder_path in cache['folders']:
        # folder_path = folder_info['path']
        if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
            results.append(f"{os.path.basename(folder_path)} (Folder)")
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
# scan_button.config(command=start_scan)

# # Start the auto scan if enabled
# if auto_scan_var.get():
#     start_auto_scan()
    
# Start the scanning process automatically
start_scan()

# Start the GUI event loop
root.mainloop()
import os 
import glob
import json
import threading
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

# # Create the Start Scan button
# scan_button = tk.Button(root, text="Start Scan")
# scan_button.pack(padx=10, pady=10)

# # Create the Auto Scan checkbox
# auto_scan_var = tk.BooleanVar()
# auto_scan_var.set(True)
# auto_scan_checkbox = tk.Checkbutton(root, text="Auto Scan on Start-up", variable=auto_scan_var)
# auto_scan_checkbox.pack(padx=10, pady=10)

# Define the scanning process
# Define a function to scan for new media files and add to cache
def scan_files():
    for root, dirs, files in os.walk('/', topdown=True):
        # Exclude system folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for extension in media_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['media']:
                    cache['media'].append(file)
                    print(f"New media file found: {file}")
        for extension in doc_extensions:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['docs']:
                    cache['docs'].append(file)
                    print(f"New document found: {file}")
        for folder in dirs:
            if folder not in cache['folders']:
                cache['folders'].append(folder)
                print(f"New folder found: {os.path.join(root, folder)}")

    # Save the updated cache file
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
# Start the scanning process in a separate thread
def start_scan():
    thread = threading.Thread(target=scan_files)
    thread.start()

# Define a function to search the cached file and folder names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs']:
        if query.lower() in os.path.basename(file).lower() and not any(exclude_folder in os.path.dirname(file) for exclude_folder in exclude_folders):
            file_type = os.path.splitext(file)[1][1:].upper()
            results.append(f"{os.path.basename(file)} ({file_type})")
    for folder_path in cache['folders']:
        # folder_path = folder_info['path']
        if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
            results.append(f"{os.path.basename(folder_path)} (Folder)")
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
# scan_button.config(command=start_scan)

# # Start the auto scan if enabled
# if auto_scan_var.get():
#     start_auto_scan()
    
# Start the scanning process automatically
start_scan()

# Start the GUI event loop
root.mainloop()
