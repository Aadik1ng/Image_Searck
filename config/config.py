# config/config.py
import os
import torch

# Device configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# CLIP model name
CLIP_MODEL_NAME = "ViT-B/32"

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images")
EMBEDDING_DIR = os.path.join(BASE_DIR, "Embeddings")
if not os.path.exists(EMBEDDING_DIR):
    os.makedirs(EMBEDDING_DIR)

EMBEDDING_FILE = os.path.join(EMBEDDING_DIR, "embedding.pt")
