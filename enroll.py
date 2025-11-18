## Create new approved user in enroll folder.
## Add approved user's .jpg files to user folder.
## Run "python enroll.py" in powershell to write new
#   user to .JSON within same directory folder.
## User will then be recognized and categorized by model# enroll_single_user.py
import os, json, base64
import numpy as np
from deepface import DeepFace

ENROLL_DIR = "enroll/lindsay"
DB_PATH = "face_db.json"

def np_to_b64(arr):
    return base64.b64encode(arr.astype(np.float32).tobytes()).decode("utf-8")

embeddings = []

for img_name in os.listdir(ENROLL_DIR):
    img_path = os.path.join(ENROLL_DIR, img_name)
    try:
        emb_obj = DeepFace.represent(
            img_path=img_path,
            model_name="ArcFace",
            enforce_detection=True
        )
        emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)
        embeddings.append(emb)
    except Exception as e:
        print(f"Skipping {img_path}: {e}")

if len(embeddings) == 0:
    raise RuntimeError("No valid face images found.")

mean_emb = np.mean(np.stack(embeddings), axis=0)
mean_emb /= np.linalg.norm(mean_emb)

with open(DB_PATH, "w") as f:
    json.dump({"Lindsay": np_to_b64(mean_emb)}, f)

print("[ENROLL] Face embedding saved for Lindsay.")
