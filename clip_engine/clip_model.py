# clip_engine/clip_model.py
import torch
import clip

from config.config import DEVICE, CLIP_MODEL_NAME

def load_clip_model():
    try:
        model, preprocess = clip.load(CLIP_MODEL_NAME, device=DEVICE)
        return model, preprocess
    except Exception as e:
        raise RuntimeError(f"Error loading CLIP model: {e}")
