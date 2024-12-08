import cv2
import pickle
import mysql.connector
from datetime import datetime
import numpy as np


with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)


conn = mysql.connector.connect(
    host="localhost",
    user="Cse299",
    password="12345",
    database="attendance_system"
)
cursor = conn.cursor()

#log attendance
def log_attendance(student_id):
    current_time = datetime.now()

   
    query = "INSERT INTO Attendance (student_id, timestamp) VALUES (%s, %s)"
    cursor.execute(query, (student_id, current_time))
    conn.commit()
    print(f"Attendance logged for student ID: {student_id} at {current_time}")


def get_student_id_by_name(name):
    query = "SELECT student_id FROM Students WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def recognize_faces_once():
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if not cam.isOpened():
        print("Error: Could not access the webcam.")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Failed to capture an image from the webcam.")
            break

        
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            face_resized = cv2.resize(face, (100, 100)).flatten()

            
            recognized_name = knn_model.predict([face_resized])[0]
            recognized_name = str(recognized_name)

            
            recognized_student_id = get_student_id_by_name(recognized_name)
            if not recognized_student_id:
                print(f"Error: Student name {recognized_name} not found in database.")
                continue  # Skip 

            # attendance for recognized 
            log_attendance(recognized_student_id)

            # Displaystudentid and name
            label = f"{recognized_student_id} - {recognized_name}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            
            cv2.imshow('Face Recognition', frame)
            cv2.waitKey(3000)  # Wait for 3 seconds before exiting
            cam.release()
            cv2.destroyAllWindows()
            print("Attendance captured. Exiting...")
            return  # Exit after capturing the first attendance

    cam.release()
    cv2.destroyAllWindows()

# Main 
if __name__ == "__main__":
    print("Starting face recognition for attendance logging...")
    recognize_faces_once()


conn.close()


