# tests/test_camera.py
import cv2

PHONE_URL = 'http://192.168.1.42:8080/video'  # Change to your phone's IP

cap = cv2.VideoCapture(PHONE_URL)

if not cap.isOpened():
    raise RuntimeError(f'Cannot open stream at {PHONE_URL}')

print('Stream opened. Press Q to quit.\n')

while True:
    ok, frame = cap.read()
    if not ok:
        print('Frame drop — retrying...')
        continue

    h, w = frame.shape[:2]
    print(f'Frame: {w}x{h}')

    cv2.imshow('DroidCam Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
