# 1
import os

path = "your_directory_path_here"

all_items = os.listdir(path)

directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

print("List of directories:", directories)
print("List of files:", files)
print("All items in the directory:", all_items)
