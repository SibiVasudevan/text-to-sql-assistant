import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.database.db_manager import DatabaseManager, DatabaseError

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text_query TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

def init_db(db_manager):
    """Creates database tables if they don't exist."""
    db_manager.execute_query(CREATE_TABLES_SQL)

    
SAMPLE_DATA_SQL = """
INSERT INTO users (username) VALUES 
    ('test_user1'),
    ('test_user2');

INSERT INTO queries (user_id, text_query, sql_query) VALUES
    (1, 'Show all users', 'SELECT * FROM users'),
    (1, 'Count queries', 'SELECT COUNT(*) FROM queries');
"""

def populate_sample_data(db_manager):
    """Populates database with sample users and queries."""
    try:
        db_manager.execute_query(SAMPLE_DATA_SQL)
        return True
    except DatabaseError:
        return False
    
if __name__ == "__main__":
    db = DatabaseManager()
    init_db(db)
    populate_sample_data(db)
    
    # Test query
    results = db.execute_query("SELECT * FROM users")
    print(results)