# Module 03: JSON CRUD Operations 🗃️

In this module, you will learn how to read and write data in JSON (JavaScript Object Notation) format using Python's built-in `json` module. JSON is the universal format for transferring structured data across APIs. 

You will build your first local database using a plain JSON file and write Create, Read, Update, and Delete (CRUD) operations.

---

## 📚 Topics Covered

1. **Serialization (`json.dump` / `json.dumps`)**: Converting Python dictionaries and lists into JSON formatted text strings.
2. **Deserialization (`json.load` / `json.loads`)**: Parsing JSON text strings back into Python dictionaries and lists.
3. **Local Database Concept**: Creating, reading, updating, and deleting records inside a local `.json` file.
4. **Validating JSON Data**: Preventing application crashes when dealing with malformed JSON text.

---

## 🗂️ Files in this Module

- `json_crud.py`: A commented tutorial illustrating the basics of `json.dumps()` and `json.loads()`, plus a complete file-based database model showing full CRUD functions. Run it using:
  ```bash
  python json_crud.py
  ```
- `exercises.py`: Practice tasks for you to complete. Run it using:
  ```bash
  python exercises.py
  ```
- `challenge.py`: A fully functional inventory system challenge built on JSON. Run it using:
  ```bash
  python challenge.py
  ```

---

## ✍️ Practice Exercises Overview

Inside `exercises.py`, you will implement:
1. `dict_to_json_string(my_dict)`: Converts a Python dictionary into a formatted JSON string.
2. `json_string_to_dict(json_str)`: Parses a JSON string back into a Python dictionary.
3. `add_entry_to_json_file(filename, entry)`: Appends an entry dictionary to a JSON list file.

---

## 🏆 Challenge Task: Inventory Management System
Inside `challenge.py`, you will complete a CLI Inventory Manager that:
- Loads a list of products from a local `inventory.json`.
- Implements:
  - **Create**: Add a new product (ID, Name, Price, Quantity).
  - **Read**: View all products or a single product by ID.
  - **Update**: Change the price or stock level of an existing product.
  - **Delete**: Remove a product from the database.
- Saves the updated inventory list back to `inventory.json`.
