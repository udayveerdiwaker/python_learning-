# ==============================================================================
# exercises.py - Practice Exercises for MySQL CRUD
# ==============================================================================
# Complete the functions below. If you have MySQL running locally, this script
# will automatically run test assertions to verify your work!

import mysql.connector
from db_connection import get_db_connection

# ------------------------------------------------------------------------------
# Exercise 1: Get Passing Students
# ------------------------------------------------------------------------------
def get_passing_students(passing_score):
    """
    Queries and returns all students whose score is greater than or equal to passing_score.
    Returns a list of dictionaries (matching students).
    
    Hint: Use: SELECT * FROM students WHERE score >= %s
    """
    # Write your code below this line
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students WHERE score >= %s", (passing_score,))
        return cursor.fetchall()
    except mysql.connector.Error:
        return []
    finally:
        cursor.close()
        conn.close()
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 2: Count Students in Subject
# ------------------------------------------------------------------------------
def count_students_by_subject(subject):
    """
    Queries the database and returns the integer count of students studying the specified subject.
    
    Hint: Use SELECT COUNT(*) FROM students WHERE subject = %s
          Use cursor.fetchone() which returns a tuple, and extract the first index.
    """
    # Write your code below this line
    conn = get_db_connection()
    if not conn:
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM students WHERE subject = %s", (subject,))
        row = cursor.fetchone()
        return row[0] if row else 0
    except mysql.connector.Error:
        return 0
    finally:
        cursor.close()
        conn.close()
    # Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 3: Update Student Subject
# ------------------------------------------------------------------------------
def update_student_subject(student_id, new_subject):
    """
    Updates the subject of the student with the specified student_id.
    Returns True if the record was successfully updated, False otherwise.
    """
    # Write your code below this line
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE students SET subject = %s WHERE id = %s", (new_subject, student_id))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
    # Write your code above this line


# ==============================================================================
# AUTOMATED TESTS (Runs only if database connection succeeds)
# ==============================================================================
if __name__ == "__main__":
    print("Checking database connection before running tests...")
    conn_check = get_db_connection()
    
    if not conn_check:
        print("\n⚠️  WARNING: Could not connect to MySQL database.")
        print("   To run the tests for this module, ensure:")
        print("   1. Your MySQL server is started (e.g. XAMPP Control Panel).")
        print("   2. You run the '04_mysql_crud/setup_db.sql' script in MySQL.")
        print("   Skipping exercises test suite.\n")
    else:
        conn_check.close()
        print("Database connected! Running tests...")
        
        # Test Exercise 1: Get Passing Students
        passing = get_passing_students(90)
        assert isinstance(passing, list), "Exercise 1 must return a list"
        # In setup_db.sql, Alice (95) and Charlie (92) should pass
        names = [s["name"] for s in passing]
        assert "Alice Smith" in names, "Alice should be in the passing list"
        assert "Charlie Brown" in names, "Charlie should be in the passing list"
        print("Exercise 1 passed! ✅")

        # Test Exercise 2: Count students by subject
        python_count = count_students_by_subject("Python")
        mysql_count = count_students_by_subject("MySQL")
        assert python_count == 2, f"Expected 2 students in Python, got {python_count}"
        assert mysql_count == 2, f"Expected 2 students in MySQL, got {mysql_count}"
        print("Exercise 2 passed! ✅")

        # Test Exercise 3: Update student subject
        # Let's insert a temp student to test update
        from mysql_crud import insert_student, delete_student
        temp_id = insert_student("Tester student", "History", 70)
        if temp_id:
            try:
                update_res = update_student_subject(temp_id, "Geography")
                assert update_res is True, "Subject update should return True"
                
                # Verify subject changed in DB
                cursor = get_db_connection().cursor(dictionary=True)
                cursor.execute("SELECT subject FROM students WHERE id = %s", (temp_id,))
                row = cursor.fetchone()
                assert row["subject"] == "Geography", f"Expected Geography, got {row['subject']}"
                cursor.close()
                print("Exercise 3 passed! ✅")
            finally:
                delete_student(temp_id)
                
        print("\nAll database exercises passed! You are a SQL Wizard! 🧙‍♂️")
