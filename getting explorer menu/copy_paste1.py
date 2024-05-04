import os
import win32clipboard

file_path = r"C:\\Users\\Geiousta\Documents\\Freelancer.text"

# Convert file path to a byte string
file_bytes = file_path.encode('utf-8')

# Open clipboard
win32clipboard.OpenClipboard()

# Empty clipboard
win32clipboard.EmptyClipboard()

# Set clipboard data
win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, file_bytes)

# Close clipboard
win32clipboard.CloseClipboard()
