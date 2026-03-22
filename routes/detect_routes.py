
from flask import Blueprint, render_template, flash
import os, time, sqlite3
import cv2
import numpy as np

# ===== Blueprint =====
detect_bp = Blueprint('detect', __name__)

# ===== Paths =====
RECOGNIZER_PATH = os.path.join("recognizer", "trainingdata.yml")

# DB path: project_root/database.db
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")

# ===== Try dlib (faster), fallback to Haar =====
USE_DLIB = False
detector = None
try:
    import dlib  # requires a working install
    detector = dlib.get_frontal_face_detector()
    USE_DLIB = True
except Exception:
    USE_DLIB = False

# Haar fallback
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ===== Helpers =====
def get_profile(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("""
        SELECT id, name, age, gender, email, problem, appointment_date
        FROM users WHERE id=?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

def load_recognizer():
    # Ensure opencv-contrib is installed
    if not hasattr(cv2, "face"):
        return None, "OpenCV contrib (cv2.face) not available. Install opencv-contrib-python."
    if not os.path.exists(RECOGNIZER_PATH):
        return None, f"Training data not found at {RECOGNIZER_PATH}."
    try:
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read(RECOGNIZER_PATH)
        return rec, None
    except Exception as e:
        return None, f"Failed to load recognizer: {e}"

# ===== Route =====
@detect_bp.route('/', methods=['GET'])
def detect_page():
    # Load recognizer
    recognizer, err = load_recognizer()
    if recognizer is None:
        return f"⚠️ {err}"

    # Open camera
    cam = cv2.VideoCapture(0)  # change to 1/2 if you have multiple cameras
    if not cam.isOpened():
        return "❌ Camera not accessible."

    # Tuning knobs
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cam.set(cv2.CAP_PROP_FPS, 30)

    CONF_THRESHOLD = 72  # a bit more lenient than 70 for real-world
    MAX_SECONDS = 8
    FRAME_SKIP = 1        # process every 2nd frame; set 0 to process all
    SCALE_DOWNSIZE = 0.75 # shrink frame to speed detection (0.6–0.8 is good)

    recognized = False
    detected_name = "Unknown"

    print("🎥 CareSync — starting fast face verification (press Q to exit).")
    start = time.time()
    frame_idx = 0

    while True:
        ok, frame = cam.read()
        if not ok:
            print("❌ Failed to read frame.")
            break

        # Optional: skip frames to reduce CPU
        if FRAME_SKIP and (frame_idx % (FRAME_SKIP + 1) != 0):
            frame_idx += 1
            cv2.imshow("🧠 CareSync - Face Verification", frame)
            if (time.time() - start) > MAX_SECONDS or (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            continue

        # Resize for speed
        if SCALE_DOWNSIZE and 0 < SCALE_DOWNSIZE < 1.0:
            frame = cv2.resize(frame, None, fx=SCALE_DOWNSIZE, fy=SCALE_DOWNSIZE, interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # lighting normalization
        gray = cv2.equalizeHist(gray)

        # --- Detect faces ---
        faces = []
        if USE_DLIB:
            # dlib returns rectangles
            drects = detector(gray, 1)  # upsample once for small faces
            for r in drects:
                faces.append((r.left(), r.top(), r.right() - r.left(), r.bottom() - r.top()))
        else:
            faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            # Crop + standardize size for recognizer
            face_roi = gray[y:y+h, x:x+w]
            if face_roi.size == 0:
                continue
            face_std = cv2.resize(face_roi, (200, 200), interpolation=cv2.INTER_CUBIC)

            # Predict
            try:
                pred_id, conf = recognizer.predict(face_std)
            except Exception as e:
                print("Predict error:", e)
                continue

            # Draw
            color = (0, 0, 255)
            label = f"❌ Not Recognized"
            if conf < CONF_THRESHOLD:
                profile = get_profile(pred_id)
                if profile:
                    name = profile[1]
                    problem = profile[5] or ""
                    appt = profile[6] or ""
                    detected_name = name
                    recognized = True
                    color = (0, 200, 0)
                    label = f"✅ {name} (conf {conf:.0f})"
                    # overlays
                    cv2.putText(frame, f"Problem: {problem[:18]}...", (x, y+h+22),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 2)
                    cv2.putText(frame, f"Appt: {appt}", (x, y+h+44),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, max(20, y-10)),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)

        cv2.imshow("🧠 CareSync - Face Verification", frame)

        frame_idx += 1
        # exit conditions
        if (time.time() - start) > MAX_SECONDS or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

        # If you want to auto-close right after first recognition:
        if recognized:
            time.sleep(0.6)  # brief pause so user sees the green box
            break

    cam.release()
    cv2.destroyAllWindows()

    # Flash + render
    if recognized:
        flash(f"✅ {detected_name} recognized successfully!", "success")
    else:
        flash("❌ Verification failed. Please try again.", "danger")

    return render_template('detect_done.html', recognized=recognized, name=detected_name)
