# setup/initializer.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from config.config import EMBEDDING_FILE, IMAGE_DIR
from helpers.utils import load_embeddings, compute_embeddings, save_embeddings, get_image_paths

def initialize():
    try:
        # Ensure directories exist
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)
        embedding_dir = os.path.dirname(EMBEDDING_FILE)
        if not os.path.exists(embedding_dir):
            os.makedirs(embedding_dir)
        
        # Load image paths from the IMAGE_DIR (which is now under static/images)
        image_paths = get_image_paths()
        
        # Load saved embeddings; if none exist and images are present, compute them
        embeddings = load_embeddings()
        if embeddings.shape[0] == 0 and image_paths:
            print("No embeddings found. Computing embeddings for images...")
            embeddings = compute_embeddings(image_paths)
            save_embeddings(embeddings)
            print("Embeddings computed and saved.")
        return embeddings, image_paths
    except Exception as e:
        print(f"Error during initialization: {e}")
        return None, []

