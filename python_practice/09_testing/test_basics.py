# test_basics.py
# Run these tests in terminal: pytest test_basics.py

# ------------------------------------------------------------------------------
# 1. Functions we want to test
# ------------------------------------------------------------------------------
def add(a: int, b: int) -> int:
    return a + b

def reverse_str(text: str) -> str:
    return text[::-1]


# ------------------------------------------------------------------------------
# 2. Pytest Unit Tests
# ------------------------------------------------------------------------------
# Pytest will scan this file and run any function starting with "test_"

def test_add_positive_numbers():
    """
    Checks if adding positive integers works.
    """
    result = add(3, 5)
    assert result == 8  # Assert check


def test_add_negative_numbers():
    """
    Checks if adding negative integers works.
    """
    assert add(-1, -1) == -2
    assert add(-5, 10) == 5


def test_reverse_string():
    """
    Checks if reverse_str correctly reverses strings.
    """
    assert reverse_str("hello") == "olleh"
    assert reverse_str("pytest") == "tsetyp"
    assert reverse_str("") == ""  # Check edge case: empty string
