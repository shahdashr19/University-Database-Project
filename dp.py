import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Database connection
def connect_db():
    return sqlite3.connect("university.db")

# Create tables if not exists
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Department (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL UNIQUE,
            building TEXT NOT NULL,
            budget REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dept_name TEXT NOT NULL,
            tot_cred INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Student_Phone (
            student_id INTEGER,
            phone_number TEXT,
            PRIMARY KEY(student_id, phone_number),
            FOREIGN KEY(student_id) REFERENCES Student(student_id)
        );

        CREATE TABLE IF NOT EXISTS Course (
            course_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            dept_name TEXT NOT NULL,
            credits INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Course_References (
            course_id TEXT,
            reference_book TEXT,
            PRIMARY KEY(course_id, reference_book),
            FOREIGN KEY(course_id) REFERENCES Course(course_id)
        );

        CREATE TABLE IF NOT EXISTS Classroom (
            building TEXT NOT NULL,
            room_number TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            PRIMARY KEY(building, room_number)
        );

        CREATE TABLE IF NOT EXISTS Time_Slot (
            time_slot_id TEXT PRIMARY KEY,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Semester_Year (
            semester_year_id INTEGER PRIMARY KEY,
            semester TEXT NOT NULL,
            year INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Section (
            course_id TEXT,
            sec_id TEXT,
            semester_year_id INTEGER,
            building TEXT NOT NULL,
            room_number TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            time_slot_id TEXT,
            PRIMARY KEY(course_id, sec_id, semester_year_id),
            FOREIGN KEY(course_id) REFERENCES Course(course_id)
        );

        CREATE TABLE IF NOT EXISTS Instructor (
            instructor_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dept_name TEXT NOT NULL,
            salary REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Advisor (
            student_id INTEGER,
            instructor_id INTEGER,
            PRIMARY KEY(student_id, instructor_id),
            FOREIGN KEY(student_id) REFERENCES Student(student_id),
            FOREIGN KEY(instructor_id) REFERENCES Instructor(instructor_id)
        );

        CREATE TABLE IF NOT EXISTS Course_Instructors (
            course_id TEXT,
            sec_id TEXT,
            semester_year_id INTEGER,
            instructor_id INTEGER,
            PRIMARY KEY(course_id, sec_id, semester_year_id, instructor_id),
            FOREIGN KEY(course_id) REFERENCES Course(course_id),
            FOREIGN KEY(instructor_id) REFERENCES Instructor(instructor_id)
        );

        CREATE TABLE IF NOT EXISTS Course_Students (
            course_id TEXT,
            sec_id TEXT,
            semester_year_id INTEGER,
            student_id INTEGER,
            PRIMARY KEY(course_id, sec_id, semester_year_id, student_id),
            FOREIGN KEY(student_id) REFERENCES Student(student_id)
        );

        CREATE TABLE IF NOT EXISTS Takes (
            student_id INTEGER,
            course_id TEXT,
            sec_id TEXT,
            semester_year_id INTEGER,
            grade TEXT,
            PRIMARY KEY(student_id, course_id, sec_id, semester_year_id),
            FOREIGN KEY(student_id) REFERENCES Student(student_id),
            FOREIGN KEY(course_id) REFERENCES Course(course_id)
        );

        CREATE TABLE IF NOT EXISTS Prereq (
            course_id TEXT,
            prereq_id TEXT,
            PRIMARY KEY(course_id, prereq_id),
            FOREIGN KEY(course_id) REFERENCES Course(course_id)
        );
        ''')
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error creating tables: {str(e)}")
    finally:
        conn.close()

# Populate the database with initial data
def populate_data():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Department Table
        departments = [
            ('Computer Science', 'Engineering', 500000.00),
            ('Mathematics', 'Science', 300000.00),
            ('Physics', 'Science', 250000.00),
            ('Biology', 'Science', 200000.00),
            ('Chemistry', 'Science', 220000.00)
        ]
        cursor.executemany("INSERT INTO Department (dept_name, building, budget) VALUES (?, ?, ?)", departments)

        # Student Table
        students = [
            (1, 'Alice', 'Smith', 'Computer Science', 90),
            (2, 'Bob', 'Johnson', 'Mathematics', 80),
            (3, 'Carol', 'Williams', 'Physics', 75),
            (4, 'David', 'Jones', 'Biology', 85),
            (5, 'Eve', 'Brown', 'Chemistry', 88)
        ]
        cursor.executemany("INSERT INTO Student (student_id, first_name, last_name, dept_name, tot_cred) VALUES (?, ?, ?, ?, ?)", students)

        # Student Phone Numbers
        student_phone = [
            (1, '555-0101'),
            (1, '555-0102'),
            (2, '555-0201'),
            (3, '555-0301'),
            (4, '555-0401')
        ]
        cursor.executemany("INSERT INTO Student_Phone (student_id, phone_number) VALUES (?, ?)", student_phone)

        # Course Table
        courses = [
            ('CS101', 'Intro to Computer Science', 'Computer Science', 3),
            ('MATH101', 'Calculus I', 'Mathematics', 4),
            # Add the rest of the course data here...
            ('SOC101', 'Sociology Basics', 'Sociology', 3)
        ]
        cursor.executemany("INSERT INTO Course (course_id, title, dept_name, credits) VALUES (?, ?, ?, ?)", courses)

        # Additional tables can be populated similarly...

        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error populating data: {str(e)}")
    finally:
        conn.close()

# Dynamic GUI logic
def main():
    current_table = None

    # Table schema definitions
    table_schemas = {
        "Department": [("dept_id", "INTEGER"), ("dept_name", "TEXT"), ("building", "TEXT"), ("budget", "REAL")],
        "Student": [("student_id", "INTEGER"), ("first_name", "TEXT"), ("last_name", "TEXT"), ("dept_name", "TEXT"), ("tot_cred", "INTEGER")],
        "Student_Phone": [("student_id", "INTEGER"), ("phone_number", "TEXT")],
        "Course": [("course_id", "TEXT"), ("title", "TEXT"), ("dept_name", "TEXT"), ("credits", "INTEGER")]
        # Add more schemas as needed...
    }

    def select_table(table_name):
        nonlocal current_table
        current_table = table_name
        label_table.config(text=f"Current Table: {current_table}")

        # Clear old fields
        for widget in fields_frame.winfo_children():
            widget.destroy()

        # Create new input fields based on the selected table schema
        for idx, (col_name, col_type) in enumerate(table_schemas[table_name]):
            Label(fields_frame, text=col_name, font=("Arial", 12), bg="#FFFACD").grid(row=idx, column=0, padx=10, pady=5)
            Entry(fields_frame, font=("Arial", 12), bg="#FFFFFF").grid(row=idx, column=1, padx=10, pady=5)

        view_records()

    def view_records():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {current_table}")
            records = cursor.fetchall()
            listbox.delete(0, END)
            for record in records:
                listbox.insert(END, record)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching records: {str(e)}")

    def add_record():
        try:
            inputs = [entry.get() for entry in fields_frame.winfo_children() if isinstance(entry, Entry)]
            placeholders = ", ".join("?" for _ in inputs)
            query = f"INSERT INTO {current_table} VALUES ({placeholders})"

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(query, inputs)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record added successfully!")
            view_records()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding record: {str(e)}")

    # Main window setup
    root = Tk()
    root.title("University Database GUI")
    root.geometry("800x600")
    root.config(bg="#FFFACD")

    # Header
    header_frame = Frame(root, bg="white", pady=10)  # Header background is now white
    header_frame.pack(fill=X)
    Label(header_frame, text="University Database", font=("Arial", 18, "bold"), bg="white", fg="#8B8000").pack()

    # Table Selection
    select_frame = Frame(root, pady=20, bg="#FFFACD")
    select_frame.pack(fill=X)
    Label(select_frame, text="Select Table:", font=("Arial", 14), bg="#FFFACD").grid(row=0, column=0, padx=10)
    for idx, table_name in enumerate(table_schemas.keys()):
        Button(select_frame, text=table_name, width=15, bg="#FFB300", fg="white", font=("Arial", 12),
               command=lambda t=table_name: select_table(t)).grid(row=0, column=idx + 1, padx=10)

    # Current Table Label
    label_table = Label(root, text="Current Table: None", font=("Arial", 16), pady=10, bg="#FFFACD")
    label_table.pack()

    # Fields
    fields_frame = Frame(root, pady=10, bg="#FFFACD")
    fields_frame.pack()

    # Action Buttons
    action_frame = Frame(root, pady=10, bg="#FFFACD")
    action_frame.pack()
    Button(action_frame, text="View Records", width=15, bg="#FFB300", fg="white", font=("Arial", 12), command=view_records).grid(row=0, column=0, padx=10)
    Button(action_frame, text="Add Record", width=15, bg="#FFB300", fg="white", font=("Arial", 12), command=add_record).grid(row=0, column=1, padx=10)

    # Records Listbox
    listbox = Listbox(root, width=100, height=10, font=("Arial", 12), bg="#FFFFFF")
    listbox.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_tables()
    populate_data()
    main()
