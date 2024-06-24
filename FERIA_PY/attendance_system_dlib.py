import cv2
import dlib
import numpy as np
import sqlite3
from datetime import datetime

# Conectar a la base de datos
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (name TEXT, date TEXT, time TEXT)''')

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()

# Cargar imágenes conocidas y aprender a reconocerlas
known_face_encodings = []
known_face_names = ["Student1", "Student2"]

for name in known_face_names:
    image = cv2.imread(f"{name}.jpg")
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = dlib.get_frontal_face_detector()(rgb_image)
    if len(boxes) > 0:
        shape = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")(rgb_image, boxes[0])
        face_encoding = np.array(dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat").compute_face_descriptor(rgb_image, shape))
        known_face_encodings.append(face_encoding)

# Iniciar captura de video
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = dlib.get_frontal_face_detector()(rgb_frame)
    face_encodings = []

    for face in face_locations:
        shape = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")(rgb_frame, face)
        face_encoding = np.array(dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat").compute_face_descriptor(rgb_frame, shape))
        face_encodings.append(face_encoding)

    for face_encoding in face_encodings:
        matches = np.linalg.norm(known_face_encodings - face_encoding, axis=1) <= 0.6
        name = "Unknown"

        if np.any(matches):
            match_index = np.argmin(np.linalg.norm(known_face_encodings - face_encoding, axis=1))
            name = known_face_names[match_index]
            mark_attendance(name)

        for face in face_locations:
            left, top, right, bottom = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
conn.close()
