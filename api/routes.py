# api/routes.py
from flask import Blueprint, request, jsonify, render_template, current_app
from helpers import utils

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    try:
        # Get image_paths from app config set during initialization
        image_paths = current_app.config.get('image_paths', [])
        return render_template("index.html", image_paths=image_paths)
    except Exception as e:
        return f"Error rendering index: {e}", 500

@routes.route('/search', methods=['POST'])
def search():
    try:
        data = request.form if request.form else request.json
        query = data.get("query", "")
        top_k = int(data.get("top_k", 5))
        # Get embeddings and image_paths from app config
        embeddings = current_app.config.get('embeddings')
        image_paths = current_app.config.get('image_paths', [])
        results = utils.search_images(query, top_k, image_embeddings=embeddings, image_paths=image_paths)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/add', methods=['POST'])
def add():
    try:
        data = request.form if request.form else request.json
        input_type = data.get("type", "").lower()  # "image" or "text"
        item = data.get("data", "")
        # Update global embeddings and image_paths in app config
        embeddings = current_app.config.get('embeddings')
        image_paths = current_app.config.get('image_paths', [])
        embeddings, image_paths, message = utils.add_embedding(input_type, item, embeddings, image_paths)
        current_app.config['embeddings'] = embeddings
        current_app.config['image_paths'] = image_paths
        return jsonify({"message": message, "image_paths": image_paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.form if request.form else request.json
        input_type = data.get("type", "").lower()  # "image" or "text"
        item = data.get("data", "")
        embeddings = current_app.config.get('embeddings')
        image_paths = current_app.config.get('image_paths', [])
        embeddings, image_paths, message = utils.delete_embedding(input_type, item, embeddings, image_paths)
        current_app.config['embeddings'] = embeddings
        current_app.config['image_paths'] = image_paths
        return jsonify({"message": message, "image_paths": image_paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
