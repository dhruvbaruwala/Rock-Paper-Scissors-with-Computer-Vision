import cv2
import random
import mediapipe as mp
import time

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Mapping fingers
def get_hand_gesture(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = fingers.count(1)

    if total_fingers == 0:
        return "Rock"
    elif total_fingers == 2:
        return "Scissors"
    elif total_fingers == 5:
        return "Paper"
    else:
        return "Unknown"

def get_winner(player, computer):
    if player == computer:
        return "Draw"
    if (player == "Rock" and computer == "Scissors") or \
       (player == "Scissors" and computer == "Paper") or \
       (player == "Paper" and computer == "Rock"):
        return "You Win!"
    return "Computer Wins!"

# Start video
cap = cv2.VideoCapture(0)

game_started = False
timer = 0
result = ""
computer_move = ""

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    player_move = "Waiting..."

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            player_move = get_hand_gesture(hand_landmarks)

    # Start countdown for move
    if game_started:
        elapsed = time.time() - timer
        cv2.putText(frame, f"Show move in: {int(3 - elapsed)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if elapsed >= 3:
            game_started = False
            computer_move = random.choice(["Rock", "Paper", "Scissors"])
            result = get_winner(player_move, computer_move)

    else:
        cv2.putText(frame, "Press 's' to start", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display moves and result
    cv2.putText(frame, f"Player: {player_move}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"Computer: {computer_move}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Result: {result}", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Rock Paper Scissors", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        game_started = True
        timer = time.time()
        result = ""
        computer_move = ""

    elif key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
