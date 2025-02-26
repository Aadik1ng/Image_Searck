# init/initialize.py
from database.db import Database
from data.table_names import IMAGE_EMBEDDINGS_TABLE

def initialize_db():
    db = Database.get_instance()
    try:
        db.execute_query(f"""
            CREATE TABLE IF NOT EXISTS {IMAGE_EMBEDDINGS_TABLE} (
            id SERIAL PRIMARY KEY,
            embedding VECTOR(512),  -- Adjust this dimension based on the embedding size
            image_path TEXT NOT NULL
        );
        """)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")

if __name__ == '__main__':
    initialize_db()
