# 1
import os

path = "your_directory_path_here"

all_items = os.listdir(path)

directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

print("List of directories:", directories)
print("List of files:", files)
print("All items in the directory:", all_items)


# 2 
import os

path = input("Enter path: ")
print(f"Path: {path}")
print(f"Exists: {os.path.exists(path)}")
print(f"Readable: {os.access(path, os.R_OK)}")
print(f"Writable: {os.access(path, os.W_OK)}")
print(f"Executable: {os.access(path, os.X_OK)}")


# 3
import os

path = input("Enter path: ")
if os.path.exists(path):
    print("The path exists.")
    print("Directory part:", os.path.dirname(path))
    print("Filename part:", os.path.basename(path))
else:
    print("The path does not exist.")


# 4
    file_path = input("Enter file path: ")
try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        print("Number of lines:", len(lines))
except FileNotFoundError:
    print("File not found.")


# 5
file_path = input("Enter file path: ")
data = ["Apple", "Banana", "Cherry"]
try:
    with open(file_path, "w") as file:
        for item in data:
            file.write(item + "\n")
    print("List written to file.")
except Exception as e:
    print("Error:", e)


# 6
import string

for letter in string.ascii_uppercase:
    file_name = letter + ".txt"
    try:
        with open(file_name, "w") as file:
            file.write("This is file " + file_name + "\n")
        print("Created:", file_name)
    except Exception as e:
        print("Error creating", file_name, ":", e)


# 7
source_file = input("Enter source file path: ")
destination_file = input("Enter destination file path: ")

try:
    with open(source_file, "r") as src:
        content = src.read()
    with open(destination_file, "w") as dest:
        dest.write(content)
    print("File copied successfully.")
except FileNotFoundError:
    print("Source file not found.")
except Exception as e:
    print("Error:", e)


# 8
import os

file_path = input("Enter file path to delete: ")

if os.path.exists(file_path):
    if os.access(file_path, os.W_OK):
        try:
            os.remove(file_path)
            print("File deleted successfully.")
        except Exception as e:
            print("Error deleting file:", e)
    else:
        print("No write permission to delete the file.")
else:
    print("File does not exist.")
