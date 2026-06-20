# Module 02: File Handling 📂

In this module, you will learn how to read data from files and write data to files using Python. File handling allows programs to persist data after they are closed, which is the precursor to databases.

---

## 📚 Topics Covered

1. **Opening and Closing Files**: Using Python's built-in `open()` function.
2. **Context Managers (`with` statement)**: The modern, safe way to handle files without worrying about manually closing them (preventing memory leaks).
3. **Reading Files**: Reading whole files (`read()`), reading line by line (`readline()`), or reading all lines into a list (`readlines()`).
4. **Writing and Appending Files**: Understanding write mode (`'w'`), which overwrites files, and append mode (`'a'`), which adds to the end.
5. **Handling CSV Files**: Reading structured data using Python's built-in `csv` module.
6. **Error Handling**: Using `try-except` blocks to catch errors if a file does not exist.

---

## 🗂️ Files in this Module

- `file_ops.py`: A commented tutorial demonstrating text file reads/writes and CSV interactions. Run it using:
  ```bash
  python file_ops.py
  ```
- `exercises.py`: Practice tasks for you to complete. Automated assertions verify your functions! Run it using:
  ```bash
  python exercises.py
  ```
- `challenge.py`: A real-world challenge to parse a raw web server access log file and extract statistics. Run it using:
  ```bash
  python challenge.py
  ```

---

## ✍️ Practice Exercises Overview

Inside `exercises.py`, you will implement:
1. `write_name_to_file(filename, name)`: Writes a name to a text file.
2. `read_first_line(filename)`: Safely reads and returns the first line of a file, returning `None` if the file doesn't exist.
3. `count_word_occurrences(filename, word)`: Counts how many times a specific word appears in a text file (case-insensitive).

---

## 🏆 Challenge Task: Web Server Log Parser
Inside `challenge.py`, you will parse a server access log file (`server_logs.txt`) that gets automatically generated. You need to:
1. Scan each line in the log.
2. Track the number of `INFO`, `WARNING`, and `ERROR` messages.
3. Extract and list all warning/error messages to a separate report file named `error_report.txt`.
