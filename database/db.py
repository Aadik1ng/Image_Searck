# database/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from data.env import POSTGRES_URL

class Database:
    _instance = None

    def __init__(self):
        self.conn = psycopg2.connect(POSTGRES_URL, cursor_factory=RealDictCursor)
        self.conn.autocommit = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def get_connection(self):
        return self.conn

    def execute_query(self, query, params=None):
        """Executes a database query with exception handling."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return None
