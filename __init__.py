import sqlite3

DB_FILE = 'expenses.db'

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        payment_type TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
    print("Database and table created successfully.")
