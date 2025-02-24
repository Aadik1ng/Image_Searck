# helpers/utils.py
import os
import torch
import glob
from PIL import Image
import clip

from config.config import DEVICE, EMBEDDING_FILE, IMAGE_DIR
from clip_engine.clip_model import load_clip_model

# Load the CLIP model once for all helper functions
try:
    model, preprocess = load_clip_model()
except Exception as e:
    print(e)
    model, preprocess = None, None

def load_embeddings(file_path=EMBEDDING_FILE):
    try:
        print(f"Loading embeddings from {file_path}...")
        if os.path.exists(file_path):
            embeddings_dict = torch.load(file_path)
            print("Embeddings loaded successfully.")
            return embeddings_dict.get('embeddings', torch.empty((0, 512)))
        print("No embeddings found, returning empty tensor.")
        return torch.empty((0, 512))
    except Exception as e:
        print(f"Error loading embeddings: {e}")
        return torch.empty((0, 512))

def save_embeddings(embeddings, file_path=EMBEDDING_FILE):
    try:
        print(f"Saving embeddings to {file_path}...")
        embeddings_dict = {'embeddings': embeddings}
        torch.save(embeddings_dict, file_path)
        print("Embeddings saved successfully.")
    except Exception as e:
        print(f"Error saving embeddings: {e}")

def compute_embeddings(image_paths):
    image_embeddings = []
    for path in image_paths:
        try:
            image = Image.open(path).convert("RGB")
            image_input = preprocess(image).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                embedding = model.encode_image(image_input)
            image_embeddings.append(embedding.cpu())
        except Exception as e:
            print(f"Error processing image {path}: {e}")
    if image_embeddings:
        print(f"Computed embeddings for {len(image_embeddings)} images.")
        return torch.cat(image_embeddings, dim=0)
    print("No embeddings computed.")
    return torch.empty((0, 512))

def compute_text_embedding(query):
    try:
        print(f"Computing text embedding for query: {query}")
        text_input = clip.tokenize([query]).to(DEVICE)
        with torch.no_grad():
            query_embedding = model.encode_text(text_input)
        print("Text embedding computed successfully.")
        return query_embedding.cpu()
    except Exception as e:
        print(f"Error computing text embedding for query '{query}': {e}")
        return None

def cosine_similarity(a, b):
    try:
        print("Computing cosine similarity...")
        a_norm = a / a.norm(dim=-1, keepdim=True)
        b_norm = b / b.norm(dim=-1, keepdim=True)
        similarity = (a_norm * b_norm).sum(dim=-1)
        print("Cosine similarity computed.")
        return similarity
    except Exception as e:
        print(f"Error computing cosine similarity: {e}")
        return None

def search_images(query, top_k=5, image_embeddings=None, image_paths=None):
    try:
        print(f"Searching for top {top_k} images for query: {query}")
        if image_embeddings is None or image_embeddings.shape[0] == 0:
            print("No image embeddings available.")
            return []
        query_embedding = compute_text_embedding(query)
        if query_embedding is None:
            return []
        sims = cosine_similarity(query_embedding, image_embeddings)
        top_indices = sims.topk(top_k).indices.numpy()
        print(f"Top {top_k} images found.")
        return [{"path": image_paths[i], "similarity": sims[i].item()} for i in top_indices]
    except Exception as e:
        print(f"Error searching images: {e}")
        return []

def add_embedding(input_type, data, embeddings, image_paths):
    try:
        print(f"Adding embedding for {input_type}...")
        if input_type == "image":
            try:
                image_input = Image.open(data).convert("RGB")
                image_input = preprocess(image_input).unsqueeze(0).to(DEVICE)
                with torch.no_grad():
                    image_embedding = model.encode_image(image_input)
                embeddings = image_embedding.cpu() if embeddings.shape[0] == 0 else torch.cat([embeddings, image_embedding.cpu()], dim=0)
                image_paths.append(data)
                message = f"Image embedding added for {data}."
            except Exception as e:
                return embeddings, image_paths, f"Error opening image: {e}"
        elif input_type == "text":
            text_embedding = compute_text_embedding(data)
            if text_embedding is None:
                return embeddings, image_paths, "Error computing text embedding."
            embeddings = text_embedding if embeddings.shape[0] == 0 else torch.cat([embeddings, text_embedding], dim=0)
            image_paths.append(data)
            message = f"Text embedding added for query: {data}"
        else:
            return embeddings, image_paths, "Invalid input type."
        save_embeddings(embeddings)
        print(f"Embedding for {input_type} saved.")
        return embeddings, image_paths, message
    except Exception as e:
        return embeddings, image_paths, f"Error in add_embedding: {e}"

def delete_embedding(input_type, data, embeddings, image_paths):
    try:
        print(f"Deleting embedding for {input_type}...")
        if data in image_paths:
            index = image_paths.index(data)
            embeddings = torch.cat([embeddings[:index], embeddings[index+1:]], dim=0)
            image_paths.pop(index)
            save_embeddings(embeddings)
            print(f"Embedding for {input_type} deleted for {data}.")
            return embeddings, image_paths, f"Embedding for {input_type} deleted successfully!"
        print(f"{input_type.capitalize()} not found for {data}.")
        return embeddings, image_paths, f"{input_type.capitalize()} not found."
    except Exception as e:
        return embeddings, image_paths, f"Error in delete_embedding: {e}"

def get_image_paths(directory=IMAGE_DIR):
    try:
        return glob.glob(os.path.join(directory, "*.jpg"))
    except Exception as e:
        print(f"Error getting image paths: {e}")
        return []
