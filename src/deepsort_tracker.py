# deepsort_tracker.py
import cv2
import config

# Install with: pip install deep-sort-realtime
from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortTracker:
    """
    Wraps DeepSORT to assign persistent person IDs across frames.

    At session start, the rover asks the user to stand in front of it.
    The first detected person gets their ID stored as the target.
    After that, DeepSORT re-identifies them even through occlusion or crowd.

    DroidCam is used to capture the initial frame that locks in the user's ID.
    """

    def __init__(self):
        self._tracker = DeepSort(max_age=30)
        self._target_id = None

    def lock_target(self, frame):
        """
        Call this once at startup with the user standing in front of the camera.
        Stores the ID of the first detected person as the follow target.
        Returns True if a target was successfully locked.
        """
        if frame is None:
            return False

        tracks = self._tracker.update_tracks(
            self._frame_to_detections(frame), frame=frame
        )

        for track in tracks:
            if not track.is_confirmed():
                continue
            self._target_id = track.track_id
            print(f'[deepsort] Target locked — ID: {self._target_id}')
            return True

        return False

    def get_target_bbox(self, frame):
        """
        Returns the bounding box (x1, y1, x2, y2) of the target person
        in the current frame, or None if they're not visible.
        """
        if frame is None or self._target_id is None:
            return None

        tracks = self._tracker.update_tracks(
            self._frame_to_detections(frame), frame=frame
        )

        for track in tracks:
            if track.is_confirmed() and track.track_id == self._target_id:
                ltrb = track.to_ltrb()
                return tuple(map(int, ltrb))  # (x1, y1, x2, y2)

        return None  # Target not visible this frame — DeepSORT will re-identify

    def _frame_to_detections(self, frame):
        """
        Converts a raw frame into the detection format DeepSORT expects.
        Uses background subtraction as a lightweight detector — you can
        replace this with YOLO detections for better accuracy.
        Format per detection: ([x, y, w, h], confidence, class_label)
        """
        h, w = frame.shape[:2]
        # Placeholder full-frame detection — replace with YOLO boxes in practice
        return [([0, 0, w, h], 0.9, 'person')]

    @property
    def has_target(self):
        return self._target_id is not None
