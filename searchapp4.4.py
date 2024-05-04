import os 
import subprocess
import glob
import json
import shutil
import threading
import pyperclip
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
                   'Intel', 'AMD', 'NVIDIA','ProgramData', '.']

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
root.geometry("800x600")
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
treeview = ttk.Treeview(root, show='headings')
# Define the columns for the treeview
treeview["columns"] = ("Path","Name", "Type", "Size")
treeview.column("#0", width=0, stretch=tk.NO)
treeview.column("Path", width=0, stretch=tk.NO)
treeview.column("Name", anchor=tk.W, width=340)
treeview.column("Type", anchor=tk.CENTER, width=30)
# treeview.column("Path", anchor=tk.W, width=300)
treeview.column("Size", anchor=tk.CENTER, width=30)

# Create the header row in the treeview
treeview.heading("#0", text="", anchor=tk.W)
treeview.heading("Path", text="Path", anchor=tk.W)
treeview.heading("Name", text="Name", anchor=tk.W)
treeview.heading("Type", text="Type", anchor=tk.W)
# treeview.heading("Path", text="Path", anchor=tk.W)
treeview.heading("Size", text="Size", anchor=tk.W)
treeview.pack(side=tk.TOP,expand=100, fill=tk.BOTH, pady=10, padx=10)
def on_right_click(event):
    global data_results, data_path, data_type, data_name
    # Get the row that was clicked
    row_id = event.widget.identify_row(event.y)
    if row_id:
        # Select the row that was clicked
        print(row_id)
        event.widget.selection_set(row_id)
        item = treeview.selection()
        # Display the context menu
        context_menu.post(event.x_root, event.y_root)
        for i in item:
            try:
                global selected_item, data_
                data_ = treeview.item(i, 'values')
                data_path, data_name, data_type =data_[0], data_[1], data_[2]
                print("this is the data from right_click :", data_)
                
            except IndexError:
                pass
        
def delete_item():
    for item_data in data_results:
        item_path, item_name = item_data['path'], item_data['type']
        print(f"{item_data['path']},{item_data['type']}\n")
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete {item_name}?")
        if confirm:
            if item_path == True:
                try:
                    shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error deleting folder: {e}")
            else:
                try:
                    os.remove(item_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")

            # Remove item from cache
            for i, cache_item in enumerate(cache):
                if cache_item['path'] == {os.path.join(root, item_data)}:
                    del cache[i]
                    break
            
            

def open_in_file_location():
    # Open the selected item's file location
    if os.path.exists(data_path):
        print(f"{data_path}, {data_type}\n")
        if data_type == "FOLDER":
            folder_path = os.path.dirname(os.path.abspath(data_path))
            os.startfile(f'"{folder_path}"')
            print('Inside the folder section')
            # os.startfile(f'/select,"{folder_path}"')
        elif data_type != "FOLDER":
            print('Inside the file section')
            os.startfile(os.path.join(os.path.dirname(data_path)))
                
    else:
        print('Path Does Not Exist...........')
def play_items():
    if os.path.exists(data_path):
        if data_type != "FOLDER":
            #Use code below if you want to open and play the file 
            os.startfile(os.path.join(os.path.dirname(data_path), data_name)) 
    else:
        print('Path Does Not Exist...........')
def copy_items():
    # Copy the selected items to the clipboard
    for item_data in data_results:
        item_path, item_name, item_type = item_data['path'], item_data['name'], item_data['type'], 
        if os.path.isdir(item_path):
            # Create a temporary directory
            temp_dir = shutil.make_archive("temp", "zip", item_path)

            # Read the contents of the temporary directory
            with open(temp_dir, "rb") as f:
                file_contents = f.read()

            # Copy the contents of the temporary directory to the system clipboard
            pyperclip.copy(file_contents)

            # Remove the temporary directory
            os.remove(temp_dir)
            # root.clipboard_clear()
            # root.clipboard_append(item_path)
            print("Folder copied to system clipboard.")
        else:
            print("Folder does not exist.")
# Create the context menu
context_menu = tk.Menu(treeview, tearoff=0)
context_menu.add_command(label="Play ", command=play_items)
context_menu.add_command(label="Open location", command=open_in_file_location)
context_menu.add_command(label="Copy selected items", command=copy_items)
context_menu.add_command(label="Delete", command=delete_item)

# Bind the right-click event to the treeview
treeview.bind("<Button-3>", on_right_click)
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
        # Exclude system folders and folders that have already been scanned
        dirs[:] = [d for d in dirs if d not in exclude_folders and not d.startswith('.') and os.path.join(root, d) not in [item['path'] for item in cache['folders']]]

        for extension in media_exts:
            for file in glob.glob(os.path.join(root, extension)):
                # Skip files that have already been scanned
                if file in [item['path'] for item in cache['media']]:
                    continue
                file_info = {
                    'path': file,
                    'size': os.path.getsize(file),
                    'type': extension.split('.')[-1].upper()
                }
                cache['media'].append(file_info)
                print(f"New media file found: {file}")

        for extension in doc_exts:
            for file in glob.glob(os.path.join(root, extension)):
                # Skip files that have already been scanned
                if file in [item['path'] for item in cache['docs']]:
                    continue
                file_info = {
                    'path': file,
                    'size': os.path.getsize(file),
                    'type': extension.split('.')[-1].upper()
                }
                cache['docs'].append(file_info)
                print(f"New document found: {file}")

        for folder in dirs:
            folder_path = os.path.join(root, folder)  
            # Skip folders that have already been scanned
            if folder_path in [item['path'] for item in cache['folders']]:
                continue
            folder_info = {
                'path': folder_path,
                'size': os.path.getsize(folder_path),
                'type': 'FOLDER'
            }
            cache['folders'].append(folder_info)
            print(f"New folder found: {folder_path}")

        # Update progress bar
        progress_var.set((len(cache['media']) + len(cache['docs']) + len(cache['folders'])) / 200)
        if progress_var.get() <= 100.0:
            progress_bar.configure(style="red.Horizontal.TProgressbar")
        elif progress_var.get() <= 150.0:
            progress_bar.configure(style="yellow.Horizontal.TProgressbar")
        elif progress_var.get() >= 150.0:
            progress_bar.configure(style="green.Horizontal.TProgressbar")

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
    for key in cache:
        for file in cache[key]:
            if query.lower() in file['path'].lower():
                result = {
                    'path': file['path'],
                    'name': os.path.basename(file['path']),
                    'size': file['size'],
                    'type': file['type']
                }
                results.append(result)
    return results


# Define a function to update the search results in the GUI
def update_results():
    query = entry.get()
    results = search_files(query)
    # print(results, '\n', end="")
    # Clear the existing results in the treeview
    treeview.delete(*treeview.get_children())

    # Insert the search results into the treeview
    for result in results:
        # print(result, '\n', end="")
        # print(f"{result['path']},{result['name']}, {result['size']}, {result['type']}\n")
        file_path,file_name, file_size, file_type = result['path'],result['name'], result['size'], result['type']
        # treeview.insert("", tk.END, text="", values=(os.path.basename(file_path), file_type, file_path, f"{file_size:,} bytes"))
        treeview.insert("", tk.END, text="", values=(file_path,os.path.basename(file_path), file_type, f"{file_size:,} bytes"))
    #  In your example, {'path': '/Users\Geiousta\Desktop\Alarms', 'name': 'Alarms', 'size': 0, 'type': 'FOLDER'} is a dictionary 
    # where 'path', 'name', 'size', and 'type' are keys and 
    # their corresponding values are '/Users\Geiousta\Desktop\Alarms', 'Alarms', 0, and 'FOLDER' respectively.
    
    # Resize the columns to fit the data
    for column in treeview["columns"]:
        treeview.heading(column, text=column, command=lambda c=column: sortby(treeview, c, 0))
        treeview.column(column, )

# Define the function to sort the treeview by a column
def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    tree.heading(col, command=lambda: sortby(tree, col, int(not descending)))


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
