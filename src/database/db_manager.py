import sqlite3
from typing import List, Dict, Optional
from contextlib import contextmanager

class DatabaseManager:
    """Manages SQLite database connections and query execution.
    
    Attributes:
        db_path: Path to SQLite database file
    """
    def __init__(self, db_path: str = "sql_assistant.db"):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Creates and yields a database connection with dictionary row factory.
        Automatically closes connection after use."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
        try:
            yield conn
        finally:
            conn.close()
    
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Split and execute multiple statements
                statements = query.split(';')
                for statement in statements:
                    if statement.strip():
                        if params:
                            cursor.execute(statement, params)
                        else:
                            cursor.execute(statement)
                
                if query.strip().upper().startswith('SELECT'):
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return []
                
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Query execution failed: {str(e)}")

class DatabaseError(Exception):
    pass