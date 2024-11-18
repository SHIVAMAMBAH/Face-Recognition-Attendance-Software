import cv2
import face_recognition
import pandas as pd
import sqlite3
import datetime
import numpy as np
import os

# Connect to SQLite Database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Load known faces from the database
def load_known_faces():
    cursor.execute("SELECT name, roll_number, face_encoding FROM students")
    known_faces = cursor.fetchall()

    known_face_names = []
    known_roll_numbers = []
    known_face_encodings = []

    for name, roll, encoding_blob in known_faces:
        if encoding_blob:  # Only process rows with valid face encodings
            known_face_names.append(name)
            known_roll_numbers.append(roll)
            encoding = np.frombuffer(encoding_blob, dtype=np.float64)  # Decode the binary encoding
            known_face_encodings.append(encoding)
        else:
            print(f"Skipping {name} ({roll}) due to missing face encoding.")

    return known_face_names, known_roll_numbers, known_face_encodings

# Mark attendance function
def mark_attendance(name, roll_number, file_path, marked_attendees):
    df = pd.read_excel(file_path)

    now = datetime.datetime.now()
    current_time_str = now.strftime('%Y-%m-%d %H:%M')

    # Check if the current timestamp is already in the columns (only once)
    if current_time_str not in df.columns:
        df[current_time_str] = ''  # Add the column for the current timestamp

    # Mark attendance only once per student
    if roll_number not in marked_attendees:
        for index, row in df.iterrows():
            if row['Name'] == name or row['Roll Number'] == roll_number:
                df.at[index, current_time_str] = 'P'
            else:
                df.at[index, current_time_str] = 'A'
        marked_attendees.add(roll_number)  # Mark this student as attended

    df.to_excel(file_path, index=False)

def recognize_and_mark(camera_id=0, excel_file='attendance.xlsx'):
    known_face_names, known_roll_numbers, known_face_encodings = load_known_faces()
    video_capture = cv2.VideoCapture(camera_id)

    marked_attendees = set()  # To track students who have been marked present
    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # Timestamp column

    # Ensure the timestamp column exists only once
    df = pd.read_excel(excel_file)
    if current_time_str not in df.columns:
        df[current_time_str] = ''
        df.to_excel(excel_file, index=False)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in the current frame
        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            # Use a threshold for face distance to filter valid matches
            if face_distances[best_match_index] < 0.6:  # Threshold can be tuned
                name = known_face_names[best_match_index]
                roll_number = known_roll_numbers[best_match_index]
                mark_attendance(name, roll_number, excel_file, marked_attendees)
            else:
                name = "Unknown"

            top, right, bottom, left = face_location
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_and_mark()
