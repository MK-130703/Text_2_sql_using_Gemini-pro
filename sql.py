import sqlite3

# Connect to the database (or create it if it doesn't exist)
connection = sqlite3.connect('student.db')

# Create a cursor object to insert, update, delete, etc.
cursor = connection.cursor()

# Create the student table only if it doesn't already exist
table_info = '''CREATE TABLE IF NOT EXISTS student (
    name VARCHAR(25),
    class VARCHAR(25),
    section VARCHAR(25),
    marks INT
)'''
cursor.execute(table_info)

# Optional: clear existing records to avoid duplicate inserts
# Uncomment if you want to reset the table each time
# cursor.execute("DELETE FROM student")

# Insert records (use `INSERT OR IGNORE` or check for duplicates manually in production)
import random

# Sample names
names = [
    "John", "Jane", "Alice", "Bob", "Emily", "David", "Sophia", "James", "Olivia", "Liam",
    "Ava", "Noah", "Emma", "Lucas", "Mia", "Mason", "Isabella", "Elijah", "Amelia", "Logan",
    "Ethan", "Harper", "Alexander", "Evelyn", "Henry", "Abigail", "Jackson", "Ella", "Sebastian", "Scarlett"
]

# Generate 1000 unique records
records = []
for _ in range(1000):
    name = random.choice(names)
    student_class = str(random.randint(10, 12))
    section = random.choice(['A', 'B', 'C'])
    marks = random.randint(50, 100)
    records.append((name, student_class, section, marks))

# Optional: print first 10 to preview
for record in records[:10]:
    print(record)

cursor.executemany("INSERT INTO student VALUES (?, ?, ?, ?)", records)

# Display all records
print("Inserted records are:")
data = cursor.execute("SELECT * FROM student")
for row in data:
    print(row)

# Commit changes and close connection
connection.commit()
connection.close()
