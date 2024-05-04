import os
import glob
import json

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

# Scan for new media files and add to cache
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

# Define a search function to search the cached file names
def search_files(query):
    results = []
    for file in cache['media'] + cache['docs']:
        if query.lower() in os.path.basename(file).lower():
            results.append(file)
    return results

# Example usage: search for all files containing "example" in their name
results = search_files("example")
print(results)
