# ==============================================================================
# basics.py - A Beginner-Friendly Introduction to Python
# ==============================================================================
# In Python, lines starting with '#' are comments. They are ignored by Python
# but are crucial for humans to understand what the code is doing.

# ------------------------------------------------------------------------------
# 1. Variables and Data Types
# ------------------------------------------------------------------------------
# A variable is a container for storing data values. In Python, you do not need
# to declare a variable's type before using it; Python figures it out automatically!

# Integer: Stores positive or negative whole numbers without decimals.
age = 25  # We assign the value 25 to the variable named 'age'

# Float: Stores decimal numbers.
price = 19.99  # We assign 19.99 to the variable 'price'

# String: Stores text, wrapped in single or double quotes.
user_name = "Alice"  # We assign the text "Alice" to 'user_name'

# Boolean: Stores either True or False. Used for logical conditions.
is_active = True  # Alice is active

# Print output to the console:
print("--- 1. Variables and Data Types ---")
print("User:", user_name, "| Age:", age, "| Active?", is_active)


# ------------------------------------------------------------------------------
# 2. Lists
# ------------------------------------------------------------------------------
# A list is an ordered collection of items. Lists can hold different types,
# and they can be modified (mutable). Lists use square brackets [].

# Creating a list of items:
shopping_cart = ["laptop", "mouse", "keyboard"]

# Accessing items: Python lists are 0-indexed (the first item is at index 0).
first_item = shopping_cart[0]  # Retrieves "laptop"
print("First item in cart:", first_item)

# Adding an item to the list:
shopping_cart.append("monitor")  # Adds "monitor" to the end of the list

# Changing an item:
shopping_cart[1] = "wireless mouse"  # Replaces "mouse" with "wireless mouse"

print("Modified cart:", shopping_cart)
print("Total items:", len(shopping_cart))  # len() returns the number of items


# ------------------------------------------------------------------------------
# 3. Dictionaries
# ------------------------------------------------------------------------------
# A dictionary is a collection of key-value pairs. Think of it like a real dictionary
# where you look up a word (the key) to find its definition (the value). Dictionaries use {}.

# Creating a dictionary:
user_profile = {
    "username": "alice_codes",
    "email": "alice@example.com",
    "login_count": 5
}

# Accessing a value using its key:
print("User Email:", user_profile["email"])

# Modifying a value:
user_profile["login_count"] = user_profile["login_count"] + 1

# Adding a new key-value pair:
user_profile["role"] = "Administrator"

print("Updated Profile:", user_profile)


# ------------------------------------------------------------------------------
# 4. Conditional Statements (Making Decisions)
# ------------------------------------------------------------------------------
# Python uses if, elif (else if), and else to run code only if certain conditions are met.
# Python uses indentation (4 spaces) to define code blocks instead of curly braces.

print("\n--- 4. Conditionals ---")
if age < 18:
    print(user_name, "is a minor.")
elif age >= 18 and age < 65:
    print(user_name, "is an adult.")
else:
    print(user_name, "is a senior citizen.")


# ------------------------------------------------------------------------------
# 5. Loops (Repeating Tasks)
# ------------------------------------------------------------------------------
# Loops are used to execute a block of code multiple times.

print("\n--- 5. Loops ---")

# For loop: Iterating over items in our shopping cart list
print("Iterating over a list:")
for item in shopping_cart:
    print("- Item in cart:", item)

# Range loop: Repeats a specific number of times (from 0 to 2)
print("Repeating 3 times using range():")
for i in range(3):
    print("  Iteration index:", i)

# While loop: Runs as long as a condition is True
counter = 3
print("Running while loop:")
while counter > 0:
    print("  Counter is:", counter)
    counter -= 1  # Equivalent to counter = counter - 1


# ------------------------------------------------------------------------------
# 6. Functions
# ------------------------------------------------------------------------------
# A function is a block of code which only runs when it is called.
# You can pass data (parameters) into a function, and it can return data as a result.

print("\n--- 6. Functions ---")

# Defining a function using the 'def' keyword:
def greet_user(name, is_new=False):
    """
    This is a docstring. It documents what the function does.
    This function greets a user.
    """
    if is_new:
        return "Welcome to the system, " + name + "! Glad you joined."
    else:
        return "Welcome back, " + name + "!"

# Calling the function and storing the result:
message_one = greet_user("Bob", is_new=True)
message_two = greet_user("Alice", is_new=False)

print(message_one)
print(message_two)


# ------------------------------------------------------------------------------
# 7. Basic Object-Oriented Programming (OOP)
# ------------------------------------------------------------------------------
# OOP is a programming paradigm that uses classes and objects.
# A Class is like a blueprint, and an Object is an instance created from that blueprint.

print("\n--- 7. Object-Oriented Programming ---")

class Smartphone:
    # The __init__ method is the constructor. It initializes the object's properties.
    # 'self' refers to the specific object we are creating.
    def __init__(self, brand, model, price):
        self.brand = brand      # Object property
        self.model = model      # Object property
        self.price = price      # Object property
        self.battery_level = 100 # Default starting property value

    # An object method (function belonging to a class)
    def use_phone(self, battery_consumed):
        # Reduce battery level, but don't let it go below 0
        self.battery_level = max(0, self.battery_level - battery_consumed)
        print(f"Used {self.brand} {self.model}. Battery level is now {self.battery_level}%.")

# Creating an instance (object) of the Smartphone class:
my_phone = Smartphone("Apple", "iPhone 15", 999.99)

# Accessing properties:
print(f"My phone brand: {my_phone.brand}, Model: {my_phone.model}")

# Calling a method:
my_phone.use_phone(15)
my_phone.use_phone(40)
