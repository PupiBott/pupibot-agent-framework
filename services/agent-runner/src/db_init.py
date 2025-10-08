import sqlite3

def initialize_database(connection=None):
    created_here = connection is None
    if created_here:
        connection = sqlite3.connect("operations.db", check_same_thread=False, timeout=30)
        connection.row_factory = sqlite3.Row  # Set row factory for dictionary-like access

    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT,
            action TEXT NOT NULL,
            payload TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()

    if created_here:
        connection.close()

if __name__ == "__main__":
    initialize_database()