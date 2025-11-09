import mysql.connector

# Connect to MySQL Server (not to a specific DB yet)
db = mysql.connector.connect(
    host="localhost",
    user="root",       # 🔁 Replace with your MySQL username
    password="Sarath@2001"    # 🔁 Replace with your MySQL password
)

cursor = db.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
print("✅ Database 'library_db' created or already exists.")

# Now connect to the newly created database
db.database = "library_db"

# Create books table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE
    )
""")

# Create issued table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued (
        book_id INT,
        user_name VARCHAR(255),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
""")

print("✅ Tables 'books' and 'issued' created or already exist.")
def display_books():
    cursor.execute("SELECT name FROM books")
    books = cursor.fetchall()
    print("\n📚 Available Books:")
    if books:
        for book in books:
            print(f"- {book[0]}")
    else:
        print("No books available.")

def add_book():
    book = input("Enter book name to add: ")
    try:
        cursor.execute("INSERT INTO books (name) VALUES (%s)", (book,))
        db.commit()
        print(f"✅ '{book}' added to library.")
    except mysql.connector.IntegrityError:
        print("⚠️ Book already exists.")

def issue_book():
    book = input("Enter book name to issue: ")
    user = input("Enter user name: ")
    cursor.execute("SELECT id FROM books WHERE name = %s", (book,))
    result = cursor.fetchone()
    if result:
        book_id = result[0]
        # Check if already issued
        cursor.execute("SELECT * FROM issued WHERE book_id = %s", (book_id,))
        if cursor.fetchone():
            print("❌ Book is already issued.")
        else:
            cursor.execute("INSERT INTO issued (book_id, user_name) VALUES (%s, %s)", (book_id, user))
            db.commit()
            print(f"📖 '{book}' issued to {user}.")
    else:
        print("❌ Book not found.")

def return_book():
    book = input("Enter book name to return: ")
    cursor.execute("SELECT id FROM books WHERE name = %s", (book,))
    result = cursor.fetchone()
    if result:
        book_id = result[0]
        cursor.execute("DELETE FROM issued WHERE book_id = %s", (book_id,))
        db.commit()
        print(f"✅ '{book}' returned.")
    else:
        print("❌ Book not found.")

def show_issued_books():
    print("\n📦 Issued Books:")
    cursor.execute("""
        SELECT b.name, i.user_name FROM issued i
        JOIN books b ON i.book_id = b.id
    """)
    issued = cursor.fetchall()
    if issued:
        for book, user in issued:
            print(f"- '{book}' → {user}")
    else:
        print("No books have been issued.")

def menu():
    while True:
        print("\n📘 Library Menu")
        print("1. Display Books")
        print("2. Add Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Show Issued Books")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_issued_books()
        elif choice == "6":
            print("Exiting... 👋")
            break
        else:
            print("❌ Invalid choice.")

menu()