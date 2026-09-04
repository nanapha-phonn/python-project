import cv2
import mediapipe as mp
import serial
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Setup serial connection to Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)
print("Serial connected:", arduino.is_open) 
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(landmarks, handedness_label):
    fingers = []
    if handedness_label == "Right":
        fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
    else:
        fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
    for tip in tip_ids[1:]:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)
    return sum(fingers)

cap = cv2.VideoCapture(0)
last_sent = -1

while True:
    ok, frame = cap.read()
    if not ok:
        print("Camera read failed")  
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = detector.detect(mp_image)

    number = 0
    if result.hand_landmarks:
        print("Hand detected!")   
        landmarks = result.hand_landmarks[0]
        handedness_label = result.handedness[0][0].category_name
        number = count_fingers(landmarks, handedness_label)
    else:
        print("No hand detected")   

    cv2.putText(frame, f"Number: {number}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if number != last_sent:
        arduino.write(f"{number}\n".encode())
        print(f"Sent to Arduino: {number}")   
        last_sent = number

    cv2.imshow("Gesture to Number", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()