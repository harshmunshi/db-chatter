import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('personal_info.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Example of how to insert data
def add_person(name, surname, email):
    try:
        cursor.execute('''
        INSERT INTO personal_info (name, surname, email)
        VALUES (?, ?, ?)
        ''', (name, surname, email))
        conn.commit()
        print("Person added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Email already exists!")

# Example of how to retrieve all records
def get_all_persons():
    cursor.execute('SELECT * FROM personal_info')
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # Add some example data
    add_person("John", "Doe", "john.doe@example.com")
    add_person("Jane", "Smith", "jane.smith@example.com")
    
    # Retrieve and display all records
    print("\nAll records:")
    for person in get_all_persons():
        print(f"ID: {person[0]}, Name: {person[1]}, Surname: {person[2]}, Email: {person[3]}")
    
    # Close the connection
    conn.close()
