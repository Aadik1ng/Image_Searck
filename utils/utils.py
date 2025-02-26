# utils/utils.py
import torch
import clip
from PIL import Image
from data.env import CLIP_MODEL_PATH

# Choose the appropriate device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the CLIP model using the environment variable
model, preprocess = clip.load(CLIP_MODEL_PATH, device=device)

def process_image_file(image_file):
    """
    Processes an image file (from request.files) and returns its normalized embedding.
    """
    image = Image.open(image_file).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()[0]

def process_text(text):
    """
    Tokenizes input text and returns its normalized embedding.
    """
    text_input = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_input)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return text_features.cpu().numpy()[0]

def save_image_file(image_file):
    """
    Saves the uploaded image file to a designated folder and returns its file path.
    """
    import os
    upload_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, image_file.filename)
    image_file.save(file_path)
    return file_path
