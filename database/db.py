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
