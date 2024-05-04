import tkinter as tk
from tkinter import ttk
import os
import io
import tarfile
import win32clipboard

root = tk.Tk()

treeview = ttk.Treeview(root)
treeview.pack()

# Add folders to the treeview
treeview.insert('', 'end', text='C:/Users/Geiousta/Desktop/Ianoh/Boom Player')
treeview.insert('', 'end', text='C:/path/to/folder2')
treeview.insert('', 'end', text='C:/path/to/folder3')

def copy_folder():
    selected_item = treeview.selection()[0]
    folder_path = treeview.item(selected_item)['text']
    folder_name = os.path.basename(folder_path)

    # Create a tarfile object and add the folder to it
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode='w') as tar:
        tar.add(folder_path, arcname=folder_name)

    # Copy the tarfile object to the clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, tar_bytes.getvalue())
    win32clipboard.CloseClipboard()

copy_button = tk.Button(root, text='Copy', command=copy_folder)
copy_button.pack()

root.mainloop()
