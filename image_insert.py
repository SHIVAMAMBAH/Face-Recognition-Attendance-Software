import face_recognition

image_path = r''
image = face_recognition.load_image_file(image_path)
encodings = face_recognition.face_encodings(image)

if len(encodings) == 0:
    print("No face found in the image.")
else:
    print("Face encoding generated successfully.")

