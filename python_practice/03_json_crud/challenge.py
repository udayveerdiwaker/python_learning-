# ==============================================================================
# challenge.py - CLI Product Inventory Manager
# ==============================================================================
# CHALLENGE: Complete the CRUD operations for managing products in a JSON database.
# Products are saved to a file named `inventory.json`.

import json
import os

DB_NAME = "inventory.json"

def load_inventory():
    """
    Loads all products from the inventory.json database.
    If the file does not exist, returns an empty list.
    """
    if not os.path.exists(DB_NAME):
        return []
    try:
        with open(DB_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Database file was corrupted. Initializing new database.")
        return []

def save_inventory(inventory):
    """
    Saves the entire inventory list back to inventory.json.
    """
    with open(DB_NAME, "w") as file:
        json.dump(inventory, file, indent=4)

def add_product(name, price, quantity):
    """
    CREATE: Adds a new product. Generates a unique, incremental ID.
    """
    inventory = load_inventory()
    
    # Generate a unique ID (Incremental)
    if inventory:
        next_id = max(p["id"] for p in inventory) + 1
    else:
        next_id = 1
        
    new_product = {
        "id": next_id,
        "name": name,
        "price": float(price),
        "quantity": int(quantity)
    }
    
    inventory.append(new_product)
    save_inventory(inventory)
    print(f"\nProduct '{name}' added successfully with ID {next_id}!")

def list_products():
    """
    READ: Prints all products in a neat, tabular layout.
    """
    inventory = load_inventory()
    if not inventory:
        print("\nNo products found in the inventory database.")
        return
        
    print("\n" + "=" * 55)
    print(f"{'ID':<5} | {'Product Name':<20} | {'Price ($)':<10} | {'Stock':<8}")
    print("=" * 55)
    for p in inventory:
        print(f"{p['id']:<5} | {p['name']:<20} | {p['price']:<10.2f} | {p['quantity']:<8}")
    print("=" * 55)

def view_product(product_id):
    """
    READ: Displays details of a single product search by ID.
    """
    inventory = load_inventory()
    for p in inventory:
        if p["id"] == product_id:
            print("\nProduct Found Details:")
            print(f"  ID:       {p['id']}")
            print(f"  Name:     {p['name']}")
            print(f"  Price:    ${p['price']:.2f}")
            print(f"  Quantity: {p['quantity']}")
            return
    print(f"\nProduct with ID {product_id} was not found.")

def update_product(product_id, new_price=None, new_qty=None):
    """
    UPDATE: Modifies price and/or quantity for a specified product ID.
    """
    inventory = load_inventory()
    found = False
    for p in inventory:
        if p["id"] == product_id:
            if new_price is not None:
                p["price"] = float(new_price)
            if new_qty is not None:
                p["quantity"] = int(new_qty)
            found = True
            break
            
    if found:
        save_inventory(inventory)
        print(f"\nProduct ID {product_id} updated successfully!")
    else:
        print(f"\nProduct with ID {product_id} was not found.")

def delete_product(product_id):
    """
    DELETE: Removes the product with the specified ID.
    """
    inventory = load_inventory()
    initial_length = len(inventory)
    # Rebuild inventory list excluding the product with product_id
    inventory = [p for p in inventory if p["id"] != product_id]
    
    if len(inventory) < initial_length:
        save_inventory(inventory)
        print(f"\nProduct ID {product_id} deleted successfully!")
    else:
        print(f"\nProduct with ID {product_id} was not found.")


# ==============================================================================
# INTERACTIVE CLI LOOP
# ==============================================================================
if __name__ == "__main__":
    print("Welcome to the Python JSON Inventory Database Manager!")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Product (Create)")
        print("2. List All Products (Read)")
        print("3. View Single Product (Read)")
        print("4. Update Product (Update)")
        print("5. Delete Product (Delete)")
        print("6. Exit")
        
        choice = input("Enter option (1-6): ").strip()
        
        if choice == "1":
            name = input("Enter product name: ").strip()
            price = input("Enter product price: ").strip()
            qty = input("Enter product quantity: ").strip()
            if name and price and qty:
                add_product(name, price, qty)
            else:
                print("All fields are required!")
                
        elif choice == "2":
            list_products()
            
        elif choice == "3":
            pid = input("Enter product ID to view: ").strip()
            if pid.isdigit():
                view_product(int(pid))
            else:
                print("Invalid product ID. Must be an integer.")
                
        elif choice == "4":
            pid = input("Enter product ID to update: ").strip()
            if pid.isdigit():
                price = input("Enter new price (leave blank to skip): ").strip()
                qty = input("Enter new quantity (leave blank to skip): ").strip()
                
                p_val = float(price) if price else None
                q_val = int(qty) if qty else None
                
                update_product(int(pid), new_price=p_val, new_qty=q_val)
            else:
                print("Invalid product ID.")
                
        elif choice == "5":
            pid = input("Enter product ID to delete: ").strip()
            if pid.isdigit():
                confirm = input(f"Are you sure you want to delete Product {pid}? (y/n): ").strip().lower()
                if confirm == 'y':
                    delete_product(int(pid))
            else:
                print("Invalid product ID.")
                
        elif choice == "6":
            print("\nExiting Inventory Manager. Data is saved in 'inventory.json'. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")

# ------------------------------------------------------------------------------
# 🏆 Extension Challenges for You:
# 1. Add a "Search Product" feature that allows users to search by partial name
#    (e.g., typing "lap" lists "laptop", "laptop charger", etc.).
# 2. Add an inventory threshold alarm: make "List All Products" highlight in red
#    or print a warning next to items where `quantity < 5`.
# ------------------------------------------------------------------------------
