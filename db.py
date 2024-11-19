
# #     print(f"Image for {name} inserted successfully!")

# # # Example: Insert an image into the database
# # insert_image('Shivam Sharma', '101', 'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-09-15 at 20.03.43.jpeg')
# # insert_image('Naitik Singhal', '102', 'C:\Users\Harshit\Downloads\new\new\images\IMG_20241020_230518.jpg')
# # insert_image('Harshit Dixit', '103', 'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-11-17 at 15.21.19.jpeg')

# # # Close the connection
# # conn.close()

# import sqlite3
# import face_recognition
# import numpy as np
# import os

# # Connect to SQLite (or create the database file if it doesn't exist)
# conn = sqlite3.connect('students.db')
# cursor = conn.cursor()

# # Update the table structure to store face encodings
# cursor.execute('''CREATE TABLE IF NOT EXISTS students (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT NOT NULL,
#                     roll_number TEXT NOT NULL,
#                     face_encoding BLOB NOT NULL
#                 )''')
# conn.commit()

# # Function to encode face from image
# def get_face_encoding(image_path):
#     image = face_recognition.load_image_file(image_path)
#     encodings = face_recognition.face_encodings(image)
#     if len(encodings) == 0:
#         raise ValueError(f"No face found in {image_path}")
#     return encodings[0]

# # Function to insert face encoding into SQLite database
# # def insert_face_encoding(name, roll_number, image_path):
# #     encoding = get_face_encoding(image_path)
# #     encoding_blob = np.array(encoding).tobytes()  # Convert encoding to binary
# #     cursor.execute("INSERT INTO students (name, roll_number, face_encoding) VALUES (?, ?, ?)",
# #                    (name, roll_number, encoding_blob))
# #     conn.commit()
# #     print(f"Face encoding for {name} inserted successfully!")

# def insert_face_encoding(name, roll_number, image_path):
#     try:
#         encoding = get_face_encoding(image_path)
#         encoding_blob = np.array(encoding).tobytes()  # Convert encoding to binary
#         cursor.execute("INSERT INTO students (name, roll_number, face_encoding) VALUES (?, ?, ?)",
#                        (name, roll_number, encoding_blob))
#         conn.commit()
#         print(f"Face encoding for {name} inserted successfully!")
#     except ValueError as e:
#         print(f"Error processing {image_path}: {e}")
#     except Exception as db_error:
#         print(f"Database error: {db_error}")


# # Example: Insert face encodings into the database
# try:
#     insert_face_encoding('Shivam Sharma', '101', r'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-09-15 at 20.03.43.jpeg')
#     insert_face_encoding('Harshit Dixit', '103', r'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-11-17 at 15.21.19.jpeg')
# except ValueError as e:
#     print(e)

# # Close the connection
# conn.close()

import sqlite3
import face_recognition
import numpy as np
import os

# Connect to SQLite (or create the database file if it doesn't exist)
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Drop and recreate the table to ensure it's correct
cursor.execute('DROP TABLE IF EXISTS students')
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_number TEXT NOT NULL,
                    face_encoding BLOB NOT NULL
                )''')
conn.commit()

# Function to encode face from image
def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        raise ValueError(f"No face found in {image_path}")
    return encodings[0]

# Function to insert face encoding into SQLite database
def insert_face_encoding(name, roll_number, image_path):
    encoding = get_face_encoding(image_path)
    encoding_blob = np.array(encoding).tobytes()  # Convert encoding to binary
    cursor.execute("INSERT INTO students (name, roll_number, face_encoding) VALUES (?, ?, ?)",
                   (name, roll_number, encoding_blob))
    conn.commit()
    print(f"Face encoding for {name} inserted successfully!")

# Example: Insert face encodings into the database
try:
    insert_face_encoding('Shivam Sharma', '101', r'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-09-15 at 20.03.43.jpeg')
    insert_face_encoding('Harshit Dixit', '103', r'C:\Users\Harshit\Downloads\new\new\images\WhatsApp Image 2024-11-17 at 15.21.19.jpeg')
except ValueError as e:
    print(e)

# Close the connection
conn.close()
