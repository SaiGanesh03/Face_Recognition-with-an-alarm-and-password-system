import face_recognition
import cv2
import numpy as np
import playsound

# Load images of the owner and other individuals
owner_image = face_recognition.load_image_file(r"C:\Users\sai\AppData\Local\Programs\Python\Python37\project\sai.jpg.jpg")
other_image = face_recognition.load_image_file(r"C:\Users\sai\AppData\Local\Programs\Python\Python37\project\saii.jpg.jpg")

# Encode face features
owner_encoding = face_recognition.face_encodings(owner_image)[0]
other_encoding = face_recognition.face_encodings(other_image)[0]

known_face_encodings = [owner_encoding]
known_face_names = ["sai"]#relpace with your name

alarm_triggered = True
correct_password = "sai"

def play_alarm_sound():
    global alarm_triggered
    #add the path where you have downloaded the alarm audio to
    playsound.playsound(r'C:\Users\sai\Pictures\Camera Roll\emergency-alarm-with-reverb-29431.mp3',block=False)
    while alarm_triggered:
        print("Enter the password to stop the alarm: ")
        entered_password = input().strip()
        print(f"Entered Password: {entered_password}")  # Debugging output  # Debugging output
        if entered_password == correct_password:
            alarm_triggered = False
            break
        else:
            print("Incorrect password. Alarm still active.")

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Find all face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "doesn't match"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw rectangle and label on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        print("owner dectected")

        if False in matches:
            play_alarm_sound()

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
