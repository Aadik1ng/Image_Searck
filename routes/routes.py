from flask import Blueprint, request, jsonify
import numpy as np
from numpy import dot
from numpy.linalg import norm
import ast
from utils.utils import process_image_file, save_image_file, process_text
from database.db import Database
from data.table_names import IMAGE_EMBEDDINGS_TABLE

api_bp = Blueprint('api', __name__)

def cosine_similarity(a, b):
    """Compute cosine similarity between two numeric vectors."""
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return dot(a, b) / (norm(a) * norm(b))

@api_bp.route('/add', methods=['POST'])
def add_image():
    """
    Accepts an image file, computes its embedding using CLIP,
    saves the image locally, and stores the embedding along with the image path in the database.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    # Save the image file and get its path
    image_path = save_image_file(image_file)
    # Reset file pointer after saving so that it can be re-read
    image_file.seek(0)
    # Compute the image embedding and ensure it's numeric
    embedding = process_image_file(image_file)
    embedding = np.array(embedding, dtype=np.float32)

    db = Database.get_instance()
    # Check for existing similar images before adding
    existing_results = db.execute_query(f"""
        SELECT id FROM {IMAGE_EMBEDDINGS_TABLE}
        ORDER BY embedding <=> %s
        LIMIT 1;
    """, (embedding.tolist(),))

    if existing_results and existing_results[0]['id']:
        return jsonify({"error": "Similar image already exists in the database"}), 409

    result = db.execute_query(f"""
        INSERT INTO {IMAGE_EMBEDDINGS_TABLE} (embedding, image_path)
        VALUES (%s, %s)
        RETURNING id;
    """, (embedding.tolist(), image_path))
    
    if result is None:
        return jsonify({"error": "Failed to add image to database"}), 500

    return jsonify({
        "message": "Image added successfully",
        "image_id": result[0]['id'],
        "image_path": image_path
    })

@api_bp.route('/delete', methods=['DELETE'])
def delete_image():
    """
    Accepts an image file, computes its embedding, and compares it against all stored embeddings.
    If the highest cosine similarity is above a defined threshold, deletes that record.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    # Compute the embedding for the provided image
    input_embedding = process_image_file(image_file)
    input_embedding = np.array(input_embedding, dtype=np.float32)

    db = Database.get_instance()
    # Find the best match using SQL
    best_match = db.execute_query(f"""
        SELECT id, image_path
        FROM {IMAGE_EMBEDDINGS_TABLE}
        ORDER BY embedding <=> %s
        LIMIT 1;
    """, (input_embedding.tolist(),))

    if not best_match:
        return jsonify({"error": "No matching image found"}), 404

    image_id = best_match[0]['id']
    image_path = best_match[0]['image_path']
    
    # Delete the best-matching record.
    cur = db.get_connection().cursor()
    cur.execute(f"DELETE FROM {IMAGE_EMBEDDINGS_TABLE} WHERE id = %s;", (image_id,))

    return jsonify({
        "message": "Image deleted successfully",
        "image_path": image_path
    })
@api_bp.route('/search', methods=['GET'])
def search_image():
    """
    Accepts a text query parameter, converts it to an embedding using CLIP,
    and compares it against all stored embeddings.
    If the highest cosine similarity is above a defined threshold, returns the corresponding image path.
    """
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Compute the text embedding using CLIP.
    query_embedding = process_text(query)
    query_embedding = np.array(query_embedding, dtype=np.float32)

    db = Database.get_instance()
    results = db.execute_query(f"""
        SELECT image_path, embedding
        FROM {IMAGE_EMBEDDINGS_TABLE}
        ORDER BY embedding <=> %s
        LIMIT 10;
    """, (query_embedding.tolist(),))
    
    if results is None or len(results) == 0:
        return jsonify({"error": "No matching image found"}), 404

    # Assuming you want to return the best match
    best_match = results[0]
    image_path = best_match['image_path']

    return jsonify({"image_path": image_path})