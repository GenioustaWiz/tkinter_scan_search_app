import os 
import glob
import json
import shutil

import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
# Define the file extensions to scan for
media_exts = ['*.mp3', '*.mp4', '*.avi', '*.mkv', '*.jpg', '*.jpeg', '*.png']
doc_exts = ['*.txt', '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx']

# Define the system folders to exclude from the scan and search
exclude_folders = ['Windows', '$RECYCLE.BIN', 
                   'System Volume Information', 
                   'Program Files', 'Program Files (x86)', 
                   'AppData', 'Local Settings', 'Temporary Internet Files',
                   'Intel', 'AMD', 'NVIDIA','ProgramData']

# Check if cache file exists and load it
cache_file = 'scan_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {'media': [], 'docs': [], 'folders': []}


# Define the columns for the Treeview
columns = ('Name', 'Type')

# Define the GUI
root = tk.Tk()
root.title("File Scanner")
# Define the icons for the Treeview rows
# folder_icon = tk.PhotoImage(file='folder.png')
# file_icon = tk.PhotoImage(file='file.png')
# image_icon = tk.PhotoImage(file='image.gif')

# video_icon = tk.PhotoImage(file='video.png')
# audio_icon = tk.PhotoImage(file='audio.png')
# document_icon = tk.PhotoImage(file='document.gif')

# Create the search box and button
search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10)
entry = tk.Entry(search_frame)
entry.pack(side=tk.LEFT, padx=5)
button = tk.Button(search_frame, text="Search")
button.pack(side=tk.LEFT, padx=5)


# Create the Treeview widget to display the search results
results_list = ttk.Treeview(root, columns=columns, show='headings')
results_list.column('Name', width=400)
results_list.column('Type', width=100)
results_list.heading('Name', text='Name')
results_list.heading('Type', text='Type')
results_list.pack(padx=10, pady=10)
def on_right_click(event):
    # Get the row that was clicked
    row_id = event.widget.identify_row(event.y)
    if row_id:
        # Select the row that was clicked
        event.widget.selection_set(row_id)

        # Display the context menu
        context_menu.post(event.x_root, event.y_root)
def delete_item():
    selection = results_list.selection()
    if selection:
        item = results_list.item(selection, 'values')
        item_type = item[0]
        # item_path = item[1]
        
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete {item}?")
        if confirm:
            if item_type == 'Folder':
                try:
                    shutil.rmtree(item)
                except Exception as e:
                    print(f"Error deleting folder: {e}")
            else:
                try:
                    os.remove(item)
                except Exception as e:
                    print(f"Error deleting file: {e}")

            # Remove item from cache
            for i, cache_item in enumerate(cache):
                if cache_item['path'] == {os.path.join(root, folder)}:
                    del cache[i]
                    break
            
            update_results()

def open_in_file_location():
    # Open the selected item's file location
    selection = results_list.selection()
    if selection:
        item = selection[0]
        file_path = results_list.set(item, "#1")
        if file_path:
            os.startfile(os.path.join(root, selection))

def copy_items():
    # Copy the selected items to the clipboard
    selection = results_list.selection()
    if selection:
        item_data = []
        for item in selection:
            item_data.append(results_list.item(item)["values"])
        item_data = "\n".join(["\t".join(item) for item in item_data])
        root.clipboard_clear()
        root.clipboard_append(item_data)
# Create the context menu
context_menu = tk.Menu(results_list, tearoff=0)
context_menu.add_command(label="Delete", command=delete_item)
context_menu.add_command(label="Open in file location", command=open_in_file_location)
context_menu.add_command(label="Copy selected items", command=copy_items)

# Bind the right-click event to the treeview
results_list.bind("<Button-3>", on_right_click)
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
    # Set up the progress bar
    progress_var.set(0)
    progress_bar.configure(style="red.Horizontal.TProgressbar")

    for root, dirs, files in os.walk('/', topdown=True):
        global folder
        # Exclude system folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for extension in media_exts:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['media']:
                    cache['media'].append(file)
                    print(f"New media file found: {file}")
        for extension in doc_exts:
            for file in glob.glob(os.path.join(root, extension)):
                if file not in cache['docs']:
                    cache['docs'].append(file)
                    print(f"New document found: {file}")
        # for folder in dirs:
        #     if folder not in exclude_folders:
        #         if folder not in cache['folders']:
        #             cache['folders'].append(folder)
        #             print(f"New folder found: {os.path.join(root, folder)}")
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if folder not in exclude_folders:
                if folder_path not in cache['folders']:
                    cache['folders'].append(folder_path)
                    folder_info = {
                        'path': folder_path,
                        'size': os.path.getsize(folder_path),
                        'modified_time': os.path.getmtime(folder_path)
                    }
                    print(f"New folder found: {folder_path}")
                    print(f"Folder info: {folder_info}")
        # Check if the root directory is a valid integer
        # # try:
        #     int(root.split(os.sep)[-1])
        # except ValueError:
        #     continue
        # # Update the progress bar
        # progress_var.set((int(root.split(os.sep)[-1]) / 255) * 100)
        # Update progress bar
        progress_var.set((len(cache['media']) + len(cache['docs']) + len(cache['folders'])) / 200)
        if progress_var.get() <= 100.0:
            progress_bar.configure(style="red.Horizontal.TProgressbar")
        elif progress_var.get() <= 150.0:
            progress_bar.configure(style="yellow.Horizontal.TProgressbar")
        elif progress_var.get() >= 150.0:
            progress_bar.configure(style="green.Horizontal.TProgressbar")

    # # Update the progress bar style
    # progress_bar.configure(style="green.Horizontal.TProgressbar")
    
    # Save the updated cache file
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    # Update progress bar
    progress_var.set(100)
    progress_bar.configure(style="green.Horizontal.TProgressbar")

# Start the scanning process in a separate thread
def start_scan():
    thread = threading.Thread(target=scan_files)
    thread.start()

# Define a function to search the cached file and folder names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs'] + cache['folders']:
        if query.lower() in os.path.basename(file).lower() and not any(exclude_folder in os.path.dirname(file) for exclude_folder in exclude_folders):
            file_type = os.path.splitext(file)[1][1:].upper()
            results.append(f"{os.path.basename(file)}")
        
    # for folder_path in cache['folders']:
    #     # folder_path = folder_info['path']
    #     if query.lower() in os.path.basename(folder_path).lower() and not any(exclude_folder in os.path.dirname(folder_path) for exclude_folder in exclude_folders):
    #         results.append(f"{os.path.basename(folder_path)} (Folder)")
    # results.sort(key=lambda x: x[1], reverse=True)   
    return results

# Define a function to update the search results in the GUI
def update_results():
    # Clear the existing search results
    results_list.delete(*results_list.get_children())
    query = entry.get()
    results = search_files(query)
    # listbox.delete(0, tk.END)
    for data in results:
        # listbox.insert(tk.END, result.split("/")[-1])
        print (data)
        # data =[data[0],data[1],data[2],data[3],data[4]]
        results_list.insert('', 'end', values=(data,)) #image=icon
        
        # if type == 'folder':
        #     icon = folder_icon
        # else:
        #     ext = os.path.splitext(name)[1].lower()
        #     # if ext in image_exts:
        #     #     icon = image_icon
        #     if ext in media_exts:
        #         # icon = video_icon
        #     elif ext in doc_exts:
        #         # icon = audio_icon
        #     # elif ext in document_exts:
        #     #     icon = document_icon
        #     else:
        #         # icon = file_icon
       


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
