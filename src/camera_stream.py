# camera_stream.py
import cv2, threading, time
import config

class CameraStream:
    """
    Threaded reader for the DroidCam / IP Webcam phone stream.
    cv2.VideoCapture.read() blocks — we run it in a background thread
    and always serve the latest frame instantly.
    """

    def __init__(self, url=config.PHONE_CAM_URL):
        self._cap = cv2.VideoCapture(url)
        self._frame = None
        self._lock = threading.Lock()
        self._running = False

    def start(self):
        if not self._cap.isOpened():
            print('[camera] failed to open stream:', config.PHONE_CAM_URL)
            return False
        self._running = True
        threading.Thread(target=self._loop, daemon=True).start()
        return True

    def _loop(self):
        while self._running:
            ok, frame = self._cap.read()
            if not ok:
                time.sleep(0.05)
                continue
            with self._lock:
                self._frame = frame

    def get(self):
        """Returns the latest frame, or None if stream hasn't started yet."""
        with self._lock:
            return None if self._frame is None else self._frame.copy()

    def stop(self):
        self._running = False
        time.sleep(0.1)
        self._cap.release()
