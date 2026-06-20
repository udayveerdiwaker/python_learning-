# ==============================================================================
# challenge.py - CLI Library Book Database System
# ==============================================================================
# CHALLENGE: Implement database-backed Library Management System using MySQL.
# This program will manage a 'books' table in the 'python_practice_db' database.

import mysql.connector
from db_connection import get_db_connection

def initialize_books_table():
    """
    Creates the 'books' table in the database if it doesn't already exist.
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        isbn VARCHAR(20) UNIQUE NOT NULL,
        title VARCHAR(250) NOT NULL,
        author VARCHAR(250) NOT NULL,
        publish_year INT NOT NULL,
        quantity INT DEFAULT 1
    );
    """
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Failed to initialize books table: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_book(isbn, title, author, publish_year, quantity):
    """
    CREATE: Adds a new book. Uses parameterized queries to avoid SQL Injection.
    """
    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor()
    sql = """
    INSERT INTO books (isbn, title, author, publish_year, quantity)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity);
    """
    values = (isbn, title, author, int(publish_year), int(quantity))
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        print(f"\nBook '{title}' added/updated successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding book: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def list_books():
    """
    READ: Displays all books currently in the database.
    """
    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT id, isbn, title, author, publish_year, quantity FROM books"
    
    try:
        cursor.execute(sql)
        books = cursor.fetchall()
        if not books:
            print("\nNo books found in the library database.")
            return
            
        print("\n" + "=" * 80)
        print(f"{'ID':<4} | {'ISBN':<13} | {'Title':<25} | {'Author':<20} | {'Year':<4} | {'Qty':<3}")
        print("=" * 80)
        for b in books:
            title_trunc = b['title'][:25]
            author_trunc = b['author'][:20]
            print(f"{b['id']:<4} | {b['isbn']:<13} | {title_trunc:<25} | {author_trunc:<20} | {b['publish_year']:<4} | {b['quantity']:<3}")
        print("=" * 80)
    except mysql.connector.Error as err:
        print(f"Error listing books: {err}")
    finally:
        cursor.close()
        conn.close()

def search_books(query):
    """
    READ: Searches for books by title or author containing the search term.
    """
    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor(dictionary=True)
    # Use LIKE for partial string matches
    sql = "SELECT id, isbn, title, author, publish_year, quantity FROM books WHERE title LIKE %s OR author LIKE %s"
    search_pattern = f"%{query}%"
    
    try:
        cursor.execute(sql, (search_pattern, search_pattern))
        books = cursor.fetchall()
        if not books:
            print(f"\nNo books matching '{query}' were found.")
            return
            
        print(f"\nSearch results for '{query}':")
        print("=" * 80)
        for b in books:
            print(f"[{b['id']}] ISBN: {b['isbn']} | {b['title']} by {b['author']} ({b['publish_year']}) - Qty: {b['quantity']}")
        print("=" * 80)
    except mysql.connector.Error as err:
        print(f"Error searching books: {err}")
    finally:
        cursor.close()
        conn.close()

def update_book_qty(book_id, new_quantity):
    """
    UPDATE: Changes the stock quantity of a book.
    """
    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor()
    sql = "UPDATE books SET quantity = %s WHERE id = %s"
    
    try:
        cursor.execute(sql, (int(new_quantity), int(book_id)))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\nBook ID {book_id} quantity updated to {new_quantity}!")
        else:
            print(f"\nBook ID {book_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error updating book: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_book(book_id):
    """
    DELETE: Removes a book record from the database.
    """
    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor()
    sql = "DELETE FROM books WHERE id = %s"
    
    try:
        cursor.execute(sql, (int(book_id),))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\nBook ID {book_id} removed from the library catalog.")
        else:
            print(f"\nBook ID {book_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error deleting book: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# ==============================================================================
# MAIN CLI CONTROLLER
# ==============================================================================
if __name__ == "__main__":
    print("Initializing Library Catalog Database...")
    if not initialize_books_table():
        print("\n⚠️  WARNING: Could not connect to MySQL server or build table.")
        print("Please start MySQL and run setup_db.sql first.")
    else:
        print("Library database online!")
        
        while True:
            print("\n--- Library Catalog CLI ---")
            print("1. Add Book (Create/Update Quantity)")
            print("2. List Catalog (Read All)")
            print("3. Search Book by Keyword (Read)")
            print("4. Update Stock Quantity (Update)")
            print("5. Delete Book Record (Delete)")
            print("6. Exit")
            
            choice = input("Enter choice (1-6): ").strip()
            
            if choice == "1":
                isbn = input("Enter ISBN (e.g. 978-0134076997): ").strip()
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                year = input("Enter Publish Year: ").strip()
                qty = input("Enter quantity to add: ").strip()
                if isbn and title and author and year and qty:
                    add_book(isbn, title, author, year, qty)
                else:
                    print("All inputs are required.")
                    
            elif choice == "2":
                list_books()
                
            elif choice == "3":
                keyword = input("Enter search keyword: ").strip()
                if keyword:
                    search_books(keyword)
                else:
                    print("Search query cannot be empty.")
                    
            elif choice == "4":
                bid = input("Enter book ID to update: ").strip()
                qty = input("Enter new quantity: ").strip()
                if bid.isdigit() and qty.isdigit():
                    update_book_qty(bid, qty)
                else:
                    print("Invalid inputs. ID and Quantity must be integers.")
                    
            elif choice == "5":
                bid = input("Enter book ID to delete: ").strip()
                if bid.isdigit():
                    confirm = input(f"Remove book ID {bid}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        delete_book(bid)
                else:
                    print("Invalid book ID.")
                    
            elif choice == "6":
                print("\nExiting Library CLI. Goodbye!")
                break
            else:
                print("Invalid selection. Choose 1-6.")

# ------------------------------------------------------------------------------
# 🏆 Extension Challenges for You:
# 1. Implement a borrowing system! Create a second table named `borrowed_books` 
#    (id, book_id, member_name, borrow_date, return_date).
# 2. Add validation to verify that ISBN contains a valid format (e.g., only digits and hyphens).
# ------------------------------------------------------------------------------
