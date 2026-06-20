# ==============================================================================
# exercises.py - Practice Exercises for JSON CRUD
# ==============================================================================
# Complete the functions below. Run this script to test your solutions!
import json
import os

# ------------------------------------------------------------------------------
# Exercise 1: Dict to JSON String
# ------------------------------------------------------------------------------
def dict_to_json_string(my_dict):
    """
    Takes a Python dictionary and returns it as a formatted JSON string (indent=2).
    """
    # Write your code below this line
    return json.dumps(my_dict, indent=2)
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 2: JSON String to Dict
# ------------------------------------------------------------------------------
def json_string_to_dict(json_str):
    """
    Takes a JSON formatted string and parses it back into a Python dictionary.
    """
    # Write your code below this line
    return json.loads(json_str)
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 3: Add Entry to JSON File List
# ------------------------------------------------------------------------------
def add_entry_to_json_file(filename, entry):
    """
    Takes a filename (string) and a dictionary representing a new entry.
    
    This function should:
    1. Check if the file exists. If it does not, initialize it with a list containing
       only the 'entry' and save.
    2. If the file exists, read the existing list, append 'entry' to that list, and
       save the entire list back to the file.
       
    Hint: Use json.load() to read and json.dump() to write.
    """
    # Write your code below this line
    if not os.path.exists(filename):
        data = [entry]
    else:
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(entry)
        
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    # Write your code above this line


# ==============================================================================
# AUTOMATED TESTS (Do not modify!)
# ==============================================================================
if __name__ == "__main__":
    print("Running tests...")
    
    # Test Exercise 1
    sample_dict = {"name": "Alice", "role": "Developer"}
    json_res = dict_to_json_string(sample_dict)
    assert isinstance(json_res, str), "Result must be a string"
    assert '"name": "Alice"' in json_res, "JSON format missing key/value"
    print("Exercise 1 passed! ✅")

    # Test Exercise 2
    sample_json = '{"course": "Python Basics", "duration_weeks": 4}'
    dict_res = json_string_to_dict(sample_json)
    assert isinstance(dict_res, dict), "Result must be a dictionary"
    assert dict_res["course"] == "Python Basics", "Dictionary values incorrectly parsed"
    assert dict_res["duration_weeks"] == 4, "Dictionary values incorrectly parsed"
    print("Exercise 2 passed! ✅")

    # Test Exercise 3
    test_json_file = "exercise_3_entries.json"
    if os.path.exists(test_json_file):
        os.remove(test_json_file)
        
    entry_1 = {"id": 1, "task": "Learn JSON"}
    entry_2 = {"id": 2, "task": "Write CRUD"}
    
    add_entry_to_json_file(test_json_file, entry_1)
    with open(test_json_file, "r") as f:
        data = json.load(f)
        assert len(data) == 1, f"Expected list of size 1, got {len(data)}"
        assert data[0]["task"] == "Learn JSON", "First entry mismatch"
        
    add_entry_to_json_file(test_json_file, entry_2)
    with open(test_json_file, "r") as f:
        data = json.load(f)
        assert len(data) == 2, f"Expected list of size 2, got {len(data)}"
        assert data[1]["task"] == "Write CRUD", "Second entry mismatch"
        
    # Clean up
    if os.path.exists(test_json_file):
        os.remove(test_json_file)
    print("Exercise 3 passed! ✅")
    
    print("\nAll exercises passed! Fantastic progress! 🎉")
