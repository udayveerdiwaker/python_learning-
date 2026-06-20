# ==============================================================================
# exercises.py - Practice Exercises for Python Basics
# ==============================================================================
# Fill in the code inside each function. Do not change the function names or
# parameter lists. Run this script to test if your code works correctly!

# ------------------------------------------------------------------------------
# Exercise 1: Calculate Rectangle Area
# ------------------------------------------------------------------------------
def calculate_area(length, width):
    """
    Takes the length and width of a rectangle and returns its area (length * width).
    If either length or width is less than or equal to 0, return 0.
    """
    # Write your code below this line
    if length <= 0 or width <= 0:
        return 0
    return length * width
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 2: Grade Calculator
# ------------------------------------------------------------------------------
def get_grade(score):
    """
    Takes a numeric test score (0 to 100) and returns a letter grade string:
    - 90 or above -> "A"
    - 80 to 89    -> "B"
    - 70 to 79    -> "C"
    - 60 to 69    -> "D"
    - Below 60    -> "F"
    """
    # Write your code below this line
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 3: Sum of Even Numbers
# ------------------------------------------------------------------------------
def sum_even_numbers(numbers_list):
    """
    Takes a list of numbers and returns the sum of only the even numbers in the list.
    Hint: Use a for loop to iterate over numbers_list, and use the modulo operator (%)
    to check if a number is even (number % 2 == 0).
    """
    # Write your code below this line
    total = 0
    for num in numbers_list:
        if num % 2 == 0:
            total += num
    return total
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 4: Add to Phonebook Dictionary
# ------------------------------------------------------------------------------
def add_to_phonebook(phonebook, name, number):
    """
    Takes a phonebook dictionary, a person's name (string), and a phone number (string).
    Adds the name and number as a key-value pair to the dictionary, and returns
    the updated phonebook dictionary.
    """
    # Write your code below this line
    phonebook[name] = number
    return phonebook
    # Write your code above this line


# ==============================================================================
# AUTOMATED TESTS (Do not modify!)
# ==============================================================================
if __name__ == "__main__":
    print("Running tests...")
    
    # Test Exercise 1
    assert calculate_area(5, 10) == 50, f"Expected 50, got {calculate_area(5, 10)}"
    assert calculate_area(0, 10) == 0, f"Expected 0, got {calculate_area(0, 10)}"
    assert calculate_area(-5, 5) == 0, f"Expected 0, got {calculate_area(-5, 5)}"
    print("Exercise 1 passed! ✅")

    # Test Exercise 2
    assert get_grade(95) == "A", f"Expected A, got {get_grade(95)}"
    assert get_grade(80) == "B", f"Expected B, got {get_grade(80)}"
    assert get_grade(72) == "C", f"Expected C, got {get_grade(72)}"
    assert get_grade(60) == "D", f"Expected D, got {get_grade(60)}"
    assert get_grade(45) == "F", f"Expected F, got {get_grade(45)}"
    print("Exercise 2 passed! ✅")

    # Test Exercise 3
    assert sum_even_numbers([1, 2, 3, 4, 5, 6]) == 12, f"Expected 12, got {sum_even_numbers([1, 2, 3, 4, 5, 6])}"
    assert sum_even_numbers([1, 3, 5]) == 0, f"Expected 0, got {sum_even_numbers([1, 3, 5])}"
    assert sum_even_numbers([]) == 0, f"Expected 0, got {sum_even_numbers([])}"
    print("Exercise 3 passed! ✅")

    # Test Exercise 4
    test_pb = {"Alice": "123-456"}
    updated_pb = add_to_phonebook(test_pb, "Bob", "987-654")
    assert updated_pb == {"Alice": "123-456", "Bob": "987-654"}, "Phonebook wasn't updated correctly"
    print("Exercise 4 passed! ✅")
    
    print("\nAll exercises passed! Outstanding job! 🎉")
