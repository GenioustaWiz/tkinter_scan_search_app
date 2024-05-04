import context_menu

# Define the file type to retrieve context menu items for
file_type = ".txt"

# Get the context menu items for the file type
menu_items = context_menu.get_menu_items(file_type)

# Print the list of menu items
for item in menu_items:
    print(item)
