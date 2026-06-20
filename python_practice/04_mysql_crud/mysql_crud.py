# ==============================================================================
# mysql_crud.py - Parameterized CRUD Operations on MySQL
# ==============================================================================
# This module demonstrates how to write safe database queries using placeholders (%s)
# to avoid SQL injection attacks, and how to manage connection lifecycles.

import mysql.connector
from db_connection import get_db_connection

# ------------------------------------------------------------------------------
# 1. CREATE: Insert a new student
# ------------------------------------------------------------------------------
def insert_student(name, subject, score):
    """
    Inserts a new student row into the students table.
    Uses parameterized query (%s) for safety.
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    # SQL query containing placeholders (%s) for parameters
    sql = "INSERT INTO students (name, subject, score) VALUES (%s, %s, %s)"
    values = (name, subject, score)
    
    try:
        cursor.execute(sql, values)
        # Commit the transaction to save changes to the database
        conn.commit()
        print(f"Created student record: {name} | ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error inserting student: {err}")
        # Rollback changes if an error occurred to keep database consistent
        conn.rollback()
        return None
    finally:
        # Always close the cursor and connection when done
        cursor.close()
        conn.close()


# ------------------------------------------------------------------------------
# 2. READ: Fetch student records
# ------------------------------------------------------------------------------
def get_all_students():
    """
    Queries and returns all students from the database as a list of dictionaries.
    """
    conn = get_db_connection()
    if not conn:
        return []
        
    # dictionary=True tells MySQL to return rows as dicts instead of tuples
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT id, name, subject, score, created_at FROM students"
    
    try:
        cursor.execute(sql)
        # fetchall() grabs all rows returned by the query
        students = cursor.fetchall()
        return students
    except mysql.connector.Error as err:
        print(f"Error fetching students: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_student_by_id(student_id):
    """
    Queries and returns a single student dict by their database ID.
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT id, name, subject, score, created_at FROM students WHERE id = %s"
    
    try:
        cursor.execute(sql, (student_id,))
        # fetchone() fetches the first matching row or returns None if no match
        student = cursor.fetchone()
        return student
    except mysql.connector.Error as err:
        print(f"Error fetching student by ID: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------------------------
# 3. UPDATE: Update a student's score
# ------------------------------------------------------------------------------
def update_student_score(student_id, new_score):
    """
    Updates the score of a student with a specific ID.
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    sql = "UPDATE students SET score = %s WHERE id = %s"
    
    try:
        cursor.execute(sql, (new_score, student_id))
        conn.commit()
        # rowcount returns the number of rows affected by the last SQL query
        if cursor.rowcount > 0:
            print(f"Updated student ID {student_id} score to {new_score}.")
            return True
        else:
            print(f"No student found with ID {student_id}.")
            return False
    except mysql.connector.Error as err:
        print(f"Error updating student score: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------------------------
# 4. DELETE: Remove a student record
# ------------------------------------------------------------------------------
def delete_student(student_id):
    """
    Deletes the student record with the specified ID.
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    sql = "DELETE FROM students WHERE id = %s"
    
    try:
        cursor.execute(sql, (student_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Deleted student record ID {student_id}.")
            return True
        else:
            print(f"No student found with ID {student_id}.")
            return False
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------------------------
# 5. RUN DEMO
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("Starting MySQL CRUD Demonstration...")
    
    # Quick check if database is online
    test_conn = get_db_connection()
    if not test_conn:
        print("Skipping CRUD demonstration because MySQL is offline.")
    else:
        test_conn.close()
        
        # 1. CREATE
        new_id = insert_student("Frank Sinatra", "Music", 98)
        
        # 2. READ All
        print("\nAll Students:")
        all_students = get_all_students()
        for s in all_students:
            print(f"  [{s['id']}] {s['name']} - Subject: {s['subject']} | Score: {s['score']}")
            
        # 3. READ Single
        if new_id:
            print(f"\nFetching newly created student (ID {new_id}):")
            single = get_student_by_id(new_id)
            print("  Result:", single)
            
            # 4. UPDATE
            update_student_score(new_id, 100)
            print("  Updated Result:", get_student_by_id(new_id))
            
            # 5. DELETE
            delete_student(new_id)
            print("  Post-delete search result:", get_student_by_id(new_id))
