import cv2
import mediapipe as mp
import numpy as np
from djitellopy import Tello

# Connect to the Tello drone
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()
tello.move_up(100)

# Set up the MediaPipe hand detection model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Set up OpenCV window
cv2.namedWindow("Tello Stream")

# Main loop
while True:
    # Get the frame from the Tello drone
    frame = tello.get_frame_read().frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands in the frame
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Draw bounding boxes around detected hands
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_coords = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in hand_landmarks.landmark])
                hand_bbox = cv2.boundingRect(hand_coords.astype(int))
                cv2.rectangle(frame, hand_bbox, (0, 255, 0), 2)

                # Check for peace sign gesture
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                if (thumb_tip.y < index_tip.y < middle_tip.y < ring_tip.y < pinky_tip.y):
                    # Perform back flip
                    tello.flip_back()
                    print("hand gesture detected")

    # Display the frame
    cv2.imshow("Tello Stream", frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break


