import sqlite3

conn = sqlite3.connect("practice.db")      # creates the file if missing
cur = conn.cursor()

# 1. Create a table
cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
""")

# 2. Insert (Create)
cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", ("Python Basics", "Asha"))
cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", ("Learning APIs", "Ravi"))
conn.commit()                               # saves the changes to the file

# 3. Select (Read)
cur.execute("SELECT * FROM books")
for row in cur.fetchall():
    print(row)

# 4. Update
cur.execute("UPDATE books SET title = ? WHERE id = ?", ("Python Basics 2", 1))
conn.commit()

# 5. Delete
cur.execute("DELETE FROM books WHERE id = ?", (2,))
conn.commit()

cur.execute("SELECT * FROM books")
print("After changes:", cur.fetchall())

conn.close()