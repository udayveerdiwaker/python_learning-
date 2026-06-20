# ==============================================================================
# db_connection.py - Reusable MySQL Connection Utility
# ==============================================================================
# This module exposes a function to get a connection to our local MySQL database.
# Before running this, make sure your MySQL server is running and setup_db.sql has been run.

import mysql.connector
from mysql.connector import Error

# Default configuration settings for a local MySQL database.
# Adjust 'user', 'password' or 'port' (default 3306) if you have customized your installation.
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",  # Standard default password is empty in XAMPP
    "database": "python_practice_db"
}

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns the connection object if successful, or None if the connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print("\n❌ Error connecting to MySQL Database!")
        print(f"Details: {e}")
        print("\n🔧 Troubleshooting Checklist:")
        print("  1. Is your MySQL server running (e.g. Apache/XAMPP started)?")
        print("  2. Did you create the database 'python_practice_db' using 'setup_db.sql'?")
        print("  3. Are the username ('root') and password ('') matching your server settings?")
        return None

if __name__ == "__main__":
    print("Testing database connection...")
    conn = get_db_connection()
    if conn:
        print("🎉 Connection successful! You are connected to the 'python_practice_db' database.")
        db_info = conn.get_server_info()
        print(f"MySQL Server version: {db_info}")
        conn.close()
        print("Connection closed.")
    else:
        print("Connection failed. Check details above.")
