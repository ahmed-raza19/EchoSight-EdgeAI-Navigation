# yolo_detector.py
from ultralytics import YOLO
import cv2

class YoloDetector:
    """
    Wraps YOLOv8n for EchoSight.
    Detects objects in the camera frame and produces spatial audio cues
    like "chair on your left" or "person in front of you".
    """

    # Only announce objects that actually matter for navigation
    INTERESTING = {
        'person', 'chair', 'couch', 'bed', 'dining table',
        'tv', 'laptop', 'backpack', 'suitcase', 'cup',
        'bottle', 'cat', 'dog', 'bicycle', 'door'
    }

    def __init__(self, model_path='models/yolov8n.pt', conf=0.4):
        self._model = YOLO(model_path)
        self._conf = conf

    def detect(self, frame):
        """
        Run inference on a frame.
        Returns a list of dicts: {label, conf, bbox=(x1, y1, x2, y2)}
        """
        if frame is None:
            return []

        results = self._model(frame, conf=self._conf, verbose=False)[0]
        out = []

        for box in results.boxes:
            cls = int(box.cls.item())
            label = self._model.names[cls]

            if label not in self.INTERESTING:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            out.append({
                'label': label,
                'conf':  float(box.conf.item()),
                'bbox':  (x1, y1, x2, y2)
            })

        return out

    def announce_text(self, detections, frame_w):
        """
        Converts detections into a single readable audio cue.
        Picks the largest (closest) detected object and gives its position.
        """
        if not detections:
            return ''

        # Largest bounding box = closest object
        det = max(
            detections,
            key=lambda d: (d['bbox'][2] - d['bbox'][0]) * (d['bbox'][3] - d['bbox'][1])
        )

        x1, _, x2, _ = det['bbox']
        cx = (x1 + x2) / 2

        if cx < frame_w * 0.4:
            side = 'on your left'
        elif cx > frame_w * 0.6:
            side = 'on your right'
        else:
            side = 'in front of you'

        return f"{det['label']} {side}"
