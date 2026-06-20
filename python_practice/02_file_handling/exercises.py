# ==============================================================================
# exercises.py - Practice Exercises for File Handling
# ==============================================================================
# Complete the functions below. Run this script to test your solutions!

# ------------------------------------------------------------------------------
# Exercise 1: Write Name to File
# ------------------------------------------------------------------------------
def write_name_to_file(filename, name):
    """
    Takes a filename (string) and a person's name (string).
    Opens the file in write mode and writes the name into the file.
    """
    # Write your code below this line
    with open(filename, "w") as file:
        file.write(name)
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 2: Safely Read First Line
# ------------------------------------------------------------------------------
def read_first_line(filename):
    """
    Takes a filename (string).
    Safely opens the file in read mode and returns the first line (stripped of newlines).
    If the file does not exist, capture the FileNotFoundError and return None.
    """
    # Write your code below this line
    try:
        with open(filename, "r") as file:
            line = file.readline()
            return line.strip() if line else ""
    except FileNotFoundError:
        return None
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 3: Count Word Occurrences
# ------------------------------------------------------------------------------
def count_word_occurrences(filename, word):
    """
    Takes a filename (string) and a search word (string).
    Reads the file content and returns the number of times the word appears in the file.
    The comparison should be case-insensitive (e.g. "python", "Python", and "PYTHON" 
    should all match).
    
    Hint: Convert the file content to lowercase and use the `.count()` string method.
    """
    # Write your code below this line
    try:
        with open(filename, "r") as file:
            content = file.read().lower()
            return content.count(word.lower())
    except FileNotFoundError:
        return 0
    # Write your code above this line


# ==============================================================================
# AUTOMATED TESTS (Do not modify!)
# ==============================================================================
if __name__ == "__main__":
    print("Running tests...")
    
    # Test Exercise 1
    test_file_1 = "exercise_1_name.txt"
    write_name_to_file(test_file_1, "John Doe")
    with open(test_file_1, "r") as f:
        assert f.read() == "John Doe", "Name was not written correctly"
    print("Exercise 1 passed! ✅")

    # Test Exercise 2
    test_file_2 = "exercise_2_lines.txt"
    with open(test_file_2, "w") as f:
        f.write("Line Number One\nLine Number Two")
    
    assert read_first_line(test_file_2) == "Line Number One", f"Expected 'Line Number One', got '{read_first_line(test_file_2)}'"
    assert read_first_line("ghost_file_xyz.txt") is None, "Should return None for non-existent file"
    print("Exercise 2 passed! ✅")

    # Test Exercise 3
    test_file_3 = "exercise_3_words.txt"
    with open(test_file_3, "w") as f:
        f.write("Python is awesome. I love python. PYTHON is fun!")
        
    assert count_word_occurrences(test_file_3, "python") == 3, f"Expected 3, got {count_word_occurrences(test_file_3, 'python')}"
    assert count_word_occurrences(test_file_3, "java") == 0, f"Expected 0, got {count_word_occurrences(test_file_3, 'java')}"
    print("Exercise 3 passed! ✅")
    
    # Clean up temporary test files
    import os
    for temp_file in [test_file_1, test_file_2, test_file_3]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    print("\nAll exercises passed! Keep up the great work! 🎉")
