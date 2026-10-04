import sqlite3


DATABASE = "mubo_memory.db"


def get_connection():
    """Create a connection to the memory database."""

    return sqlite3.connect(DATABASE)


def create_memory_table():
    """Create the memory table if it does not exist."""

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            assistant_response TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_memory(user_message, assistant_response):
    """Save a conversation to memory."""

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO memories (user_message, assistant_response)
        VALUES (?, ?)
        """,
        (user_message, assistant_response)
    )

    connection.commit()
    connection.close()


def get_memories(limit=10):
    """Return recent conversations from memory."""

    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT user_message, assistant_response
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    memories = cursor.fetchall()

    connection.close()

    return memories

def search_memories(query, limit=5):
    """Find memories that contain words from the user's query."""

    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT user_message, assistant_response
        FROM memories
        WHERE user_message LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{query}%", limit)
    )

    memories = cursor.fetchall()

    connection.close()

    return memories

def get_recent_memories(limit=5):
    """Return the most recent conversations."""

    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT user_message, assistant_response
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    memories = cursor.fetchall()

    connection.close()

    return memories
