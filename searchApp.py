import os
import glob
import json
import tkinter as tk

# Define the file extensions to scan for
media_extensions = ['*.mp3', '*.mp4', '*.avi', '*.mkv', '*.jpg', '*.jpeg', '*.png']
doc_extensions = ['*.txt', '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx']

# Check if cache file exists and load it
cache_file = 'scan_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {'media': [], 'docs': []} 

# Define a function to scan for new media files and add to cache
def scan_files():
    for root, dirs, files in os.walk('/'):
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

    # Save the updated cache file
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

# Define a function to search the cached file names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs']:
        if query.lower() in os.path.basename(file).lower():
            results.append(file)
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
    root.after(60000, start_auto_scan) # Reschedule after 1 minute

# Create the GUI
root = tk.Tk()
root.title("File Scanner")
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


# import os

# def scan_directories(root_dir):
#     for root, dirs, files in os.walk(root_dir):
#         for name in files:
#             file_path = os.path.join(root, name)
#             print(f"File: {file_path}")
#         for name in dirs:
#             dir_path = os.path.join(root, name)
#             print(f"Directory: {dir_path}")

# # Call the function, passing the root directory that you want to scan
# scan_directories("/")

