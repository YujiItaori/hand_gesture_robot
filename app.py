from flask import Flask, render_template, Response, request
import cv2
import mediapipe as mp
import os
from gesture_logic import detect_gesture

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Global for live webcam overlay
gesture_text = "None"
action_text = "None"

@app.route("/", methods=["GET", "POST"])
def index():
    global gesture_text, action_text
    gesture = gesture_text
    action = action_text
    filename = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            filename = "output_" + file.filename

            image = cv2.imread(filepath)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            with mp_hands.Hands(static_image_mode=True) as hands:
                result = hands.process(image_rgb)

                if result.multi_hand_landmarks:
                    hand_landmarks = result.multi_hand_landmarks[0]
                    gesture, action = detect_gesture(hand_landmarks.landmark)

                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    output_path = os.path.join(UPLOAD_FOLDER, filename)
                    cv2.imwrite(output_path, image)
                else:
                    gesture = "None"
                    action = "No Hand Detected"

    return render_template("index.html", filename=filename, gesture=gesture, action=action)

def generate_frames():
    global gesture_text, action_text
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        while True:
            success, frame = cap.read()
            if not success:
                break

            image = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
                gesture_text, action_text = detect_gesture(landmarks.landmark)

                cv2.putText(image, f'Gesture: {gesture_text}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f'Action: {action_text}', (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                gesture_text = "None"
                action_text = "No Hand"

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
