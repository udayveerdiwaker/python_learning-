# ==============================================================================
# json_crud.py - Serialization, Deserialization, and Local File DB CRUD
# ==============================================================================
import json
import os

# ------------------------------------------------------------------------------
# 1. JSON String Operations (dumps and loads)
# ------------------------------------------------------------------------------
# - dumps (Dump String): Converts Python dictionaries/lists into JSON strings.
# - loads (Load String): Parses a JSON string back into a Python dictionary/list.

print("--- 1. JSON String Operations ---")
developer_profile = {
    "name": "Alex",
    "languages": ["Python", "JavaScript", "SQL"],
    "is_certified": True
}

# Convert dict to JSON string:
# indent=4 formats it with pretty indentations, sort_keys sorts keys alphabetically
json_string = json.dumps(developer_profile, indent=4)
print("Serialized JSON String:")
print(json_string)

# Convert JSON string back to dict:
parsed_dict = json.loads(json_string)
print("\nParsed Back Python Dict:")
print(parsed_dict)
print("Languages List Access:", parsed_dict["languages"])


# ------------------------------------------------------------------------------
# 2. Local JSON File-Based Database CRUD Framework
# ------------------------------------------------------------------------------
# We will use 'users.json' as a local database file to store user records.
DB_FILE = "users.json"

def init_db():
    """
    Initializes the JSON database file with an empty list if it doesn't exist.
    """
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as file:
            json.dump([], file)  # Save an empty list to the file
        print(f"Database initialized: {DB_FILE}")

def read_users():
    """
    READ (GET) operation: Loads and returns the list of users from the JSON file.
    """
    init_db()
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    """
    Helper function to save the full users list back to the JSON file.
    """
    with open(DB_FILE, "w") as file:
        # indent=4 writes formatted JSON for easy human reading
        json.dump(users, file, indent=4)

def create_user(user_id, username, email):
    """
    CREATE (POST) operation: Adds a new user record.
    Returns True if added, False if the user_id already exists.
    """
    users = read_users()
    
    # Check if user ID already exists
    for u in users:
        if u["id"] == user_id:
            print(f"Error: User ID {user_id} already exists!")
            return False
            
    # Construct the new user dictionary
    new_user = {
        "id": user_id,
        "username": username,
        "email": email
    }
    
    users.append(new_user)
    save_users(users)
    print(f"User '{username}' created successfully.")
    return True

def update_user(user_id, new_email):
    """
    UPDATE (PUT) operation: Finds a user by ID and updates their email.
    Returns True if updated, False if user not found.
    """
    users = read_users()
    for u in users:
        if u["id"] == user_id:
            u["email"] = new_email
            save_users(users)
            print(f"User ID {user_id} email updated to: {new_email}")
            return True
            
    print(f"Error: User ID {user_id} not found!")
    return False

def delete_user(user_id):
    """
    DELETE operation: Removes a user from the JSON database by ID.
    Returns True if deleted, False if user not found.
    """
    users = read_users()
    for index, u in enumerate(users):
        if u["id"] == user_id:
            removed_user = users.pop(index)  # Remove the item at this index
            save_users(users)
            print(f"User ID {user_id} ('{removed_user['username']}') deleted successfully.")
            return True
            
    print(f"Error: User ID {user_id} not found!")
    return False


# ------------------------------------------------------------------------------
# 3. Running a CRUD Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Reset database for clean demo run
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    print("\n--- 2. JSON File Database CRUD Demonstration ---")
    
    # 1. CREATE users
    create_user(1, "alice", "alice@example.com")
    create_user(2, "bob", "bob@example.com")
    
    # Try adding a duplicate ID
    create_user(1, "charlie", "charlie@example.com")
    
    # 2. READ users
    current_users = read_users()
    print("\nCurrent database state:")
    print(json.dumps(current_users, indent=2))
    
    # 3. UPDATE a user
    update_user(2, "bob_new@example.com")
    
    # 4. DELETE a user
    delete_user(1)
    
    # Verify final state
    final_users = read_users()
    print("\nFinal database state:")
    print(json.dumps(final_users, indent=2))
    
    # Cleanup demo database file
    if os.path.exists(DB_FILE):
         os.remove(DB_FILE)
