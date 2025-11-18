# Lindsay Strauss 11/16/25
# face_access_control.py
import json, base64
import numpy as np
import cv2
from deepface import DeepFace
import serial
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "enroll", "face_db.json")
COM_PORT = "COM3"
BAUD_RATE = 9600
GRANT_THRESHOLD = 0.60  # adjust after testing

# help functions

def b64_to_np(s):
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

# -load embedding

with open(DB_PATH, "r") as f:
    raw_db = json.load(f)

Lindsay_Emb = b64_to_np(raw_db["Lindsay"])

# arduino serial

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("[SYSTEM] Arduino Connected.")

# face rec

def run_face_recognition():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("No camera detected.")

    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        try:
            emb_obj = DeepFace.represent(
                img_path=frame,
                model_name="ArcFace",
                enforce_detection=True
            )
            emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)

            score = cosine_similarity(emb, Lindsay_Emb)
            is_granted = score >= GRANT_THRESHOLD

            label = f"{'Lindsay' if is_granted else 'Denied'} | sim={score:.2f}"
            color = (0, 255, 0) if is_granted else (0, 0, 255)

            cv2.putText(frame, label, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if is_granted:
                print("[SYSTEM] Lindsay Verified.")
                if ser:
                    ser.write(b"APPROVED\n")

                cv2.imshow("Face Access Control", frame)   # show your face FIRST
                cv2.waitKey(1000)  # wait a second so you can see it
                break

            else:
                # show denied in real time but let loop continue
                pass

        except Exception:
            # no face detected
            pass

        # Timeout to prevent freezing when no face detected
        if time.time() - start > 10:
            print("[SYSTEM] No face detected - Access Denied.")
            ser.write(b"DENIED\n")
            break

        cv2.imshow("Face Access Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[SYSTEM] Quit manual.")
            ser.write(b"DENIED\n")
            break

    cap.release()
    cv2.destroyAllWindows()

# run immediately 

print("[SYSTEM] Ready for Face Scan.")
run_face_recognition()
