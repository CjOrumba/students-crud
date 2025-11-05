# app.py
# PostgreSQL CRUD demo for the "students" table.
# If run with no arguments, it will list all students.
# Commands:
#   python3 app.py list
#   python3 app.py add FIRST LAST EMAIL YYYY-MM-DD
#   python3 app.py update STUDENT_ID NEW_EMAIL
#   python3 app.py delete STUDENT_ID

import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# === EDIT THESE IF NEEDED ===
PG_HOST = "localhost"
PG_DB   = "students_db"
PG_USER = "postgres"          # use your pgAdmin user if different
PG_PASS = "Jay2slime"  # <-- put your actual postgres password

def get_conn():
    return psycopg2.connect(
        host=PG_HOST, dbname=PG_DB, user=PG_USER, password=PG_PASS
    )

def getAllStudents():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM students ORDER BY student_id;")
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
        for r in rows:
            print(f"[{r['student_id']}] {r['first_name']} {r['last_name']} - {r['email']} ({r['enrollment_date']})")

def addStudent(first_name, last_name, email, enrollment_date):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s) RETURNING student_id;",
            (first_name, last_name, email, enrollment_date)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"Added student with ID {new_id}")

def updateStudentEmail(student_id, new_email):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE students SET email=%s WHERE student_id=%s;", (new_email, student_id))
        conn.commit()
        print(f"Updated {cur.rowcount} record(s).")

def deleteStudent(student_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id=%s;", (student_id,))
        conn.commit()
        print(f"Deleted {cur.rowcount} record(s).")

def usage():
    print("Usage:")
    print("  python3 app.py list")
    print("  python3 app.py add FIRST LAST EMAIL YYYY-MM-DD")
    print("  python3 app.py update STUDENT_ID NEW_EMAIL")
    print("  python3 app.py delete STUDENT_ID")

def main():
    # If no args, default to list so you always see output
    if len(sys.argv) == 1:
        getAllStudents()
        return

    cmd = sys.argv[1].lower()

    if cmd == "list":
        getAllStudents()

    elif cmd == "add":
        if len(sys.argv) != 6:
            usage(); return
        _, _, first, last, email, date = sys.argv
        addStudent(first, last, email, date)

    elif cmd == "update":
        if len(sys.argv) != 4:
            usage(); return
        _, _, sid, new_email = sys.argv
        updateStudentEmail(sid, new_email)

    elif cmd == "delete":
        if len(sys.argv) != 3:
            usage(); return
        _, _, sid = sys.argv
        deleteStudent(sid)

    else:
        usage()

if __name__ == "__main__":
    try:
        main()
    except psycopg2.OperationalError as e:
        print("Database connection failed. Check PG_USER/PG_PASS/host/dbname.")
        print(e)

