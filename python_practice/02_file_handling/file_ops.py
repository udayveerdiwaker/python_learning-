# ==============================================================================
# file_ops.py - Reading, Writing, and Appending Files in Python
# ==============================================================================
import csv  # Built-in module for working with Comma Separated Values (CSV) files

# ------------------------------------------------------------------------------
# 1. Writing to a Text File (Overwrite Mode)
# ------------------------------------------------------------------------------
# We use open(filename, mode) to open a file.
# Mode 'w' stands for WRITE. It will create the file if it doesn't exist.
# WARNING: If the file already exists, 'w' will completely overwrite its content!

# The 'with' statement acts as a Context Manager. It automatically closes
# the file after the block of code finishes, even if an error occurs.
print("--- 1. Writing to a Text File ---")
with open("sample.txt", "w") as file:
    file.write("Hello World!\n")
    file.write("This is the second line of our file.\n")
    file.write("Python file handling is easy and safe.\n")

print("File 'sample.txt' written successfully.")


# ------------------------------------------------------------------------------
# 2. Reading from a Text File
# ------------------------------------------------------------------------------
# Mode 'r' stands for READ. It is the default mode if you don't specify one.

print("\n--- 2. Reading a File (All at once) ---")
with open("sample.txt", "r") as file:
    content = file.read()  # Reads the entire content as a single string
    print(content)

print("--- Reading Line by Line ---")
with open("sample.txt", "r") as file:
    # We can iterate over the file object directly using a for loop.
    # This is memory-efficient because it reads one line at a time.
    for index, line in enumerate(file, 1):
        # strip() removes the newline character (\n) from the end of the line
        print(f"Line {index}: {line.strip()}")


# ------------------------------------------------------------------------------
# 3. Appending to a Text File
# ------------------------------------------------------------------------------
# Mode 'a' stands for APPEND. It adds text to the end of the file instead of
# overwriting it. It creates the file if it does not exist.

print("\n--- 3. Appending to a File ---")
with open("sample.txt", "a") as file:
    file.write("This line was added using append mode ('a').\n")

# Verify append worked
with open("sample.txt", "r") as file:
    print(file.read())


# ------------------------------------------------------------------------------
# 4. Safe File Operations (Error Handling)
# ------------------------------------------------------------------------------
# If we try to read a file that does not exist in 'r' mode, Python raises a
# FileNotFoundError. We can use try-except to handle this gracefully.

print("--- 4. Safe File Reading ---")
non_existent_file = "ghost_file.txt"

try:
    with open(non_existent_file, "r") as file:
        print(file.read())
except FileNotFoundError:
    print(f"Oops! The file '{non_existent_file}' does not exist. Handled safely.")


# ------------------------------------------------------------------------------
# 5. Handling CSV Files (Comma Separated Values)
# ------------------------------------------------------------------------------
# CSV files are used for structured tabular data. Python's csv module simplifies
# reading and writing rows.

print("\n--- 5. Handling CSV Files ---")

# Writing to a CSV file:
csv_filename = "students.csv"
headers = ["Name", "Subject", "Score"]
rows = [
    ["Alice", "Python", "95"],
    ["Bob", "MySQL", "88"],
    ["Charlie", "FastAPI", "92"]
]

with open(csv_filename, "w", newline="") as file:
    # csv.writer takes the open file object
    writer = csv.writer(file)
    # Write the headers row:
    writer.writerow(headers)
    # Write multiple rows of data:
    writer.writerows(rows)

print(f"CSV File '{csv_filename}' written successfully.")

# Reading from a CSV file:
print("Reading CSV Data:")
with open(csv_filename, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Each 'row' is returned as a list of strings
        print(f"Student: {row[0]} | Subject: {row[1]} | Grade: {row[2]}")
