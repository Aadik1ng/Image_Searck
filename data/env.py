# data/env.py
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file if present

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://aaditya:Hxjrhao22abjbkal1Qjz@194.195.112.175:5432/face_rec_1")
CLIP_MODEL_PATH = os.getenv("CLIP_MODEL_PATH", "ViT-B/32")
DATABASE_NAME = os.getenv("DATABASE_NAME", "face_rec_1")
