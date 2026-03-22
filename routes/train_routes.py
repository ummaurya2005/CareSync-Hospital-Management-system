from flask import Blueprint, render_template, redirect
import cv2
import numpy as np
from PIL import Image
import os

train_bp = Blueprint('train', __name__, template_folder='../templates')

dataset_path = "dataset"
recognizer_path = "recognizer"
os.makedirs(recognizer_path, exist_ok=True)

@train_bp.route('/', methods=['GET', 'POST'])
def train_page():
    # Check if dataset exists
    if not os.path.exists(dataset_path) or len(os.listdir(dataset_path)) == 0:
        return "⚠️ No images found in dataset. Please register some users first."

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_and_labels(dataset_path)

    recognizer.train(faces, np.array(ids))
    recognizer.save(os.path.join(recognizer_path, "trainingdata.yml"))
    print(f"✅ Training completed on {len(ids)} samples.")
    return render_template('train_success.html', count=len(ids))


def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    faces = []
    ids = []

    for img_path in image_paths:
        gray_img = Image.open(img_path).convert('L')
        img_np = np.array(gray_img, 'uint8')
        user_id = int(os.path.split(img_path)[-1].split(".")[0])  # e.g., "1.1.jpg" → 1
        faces.append(img_np)
        ids.append(user_id)
    return faces, ids
