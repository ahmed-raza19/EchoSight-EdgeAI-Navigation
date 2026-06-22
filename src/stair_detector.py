# stair_detector.py
import RPi.GPIO as GPIO
import time, threading
import config

class StairDetector:
    """
    Detects two types of stair hazards:

    1. Downward drops — a ToF/ultrasonic sensor tilted slightly downward
       at the front of the rover. If the reading suddenly jumps past
       CLIFF_DROP_CM, there's a drop ahead (step, curb, table edge).

    2. Upward risers — heuristic from the LiDAR scan. A dense wall of
       returns directly ahead at < 0.6m likely means an upward step.
       (2D LiDAR can't distinguish a wall from a stair riser with certainty,
       so this flags it for caution and lets the user confirm with their cane.)
    """

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.CLIFF_TRIG, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(config.CLIFF_ECHO, GPIO.IN)
        self._last_drop = False
        threading.Thread(target=self._loop, daemon=True).start()

    def _read_cm(self):
        """Pulse the ultrasonic and return distance in cm."""
        GPIO.output(config.CLIFF_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(config.CLIFF_TRIG, False)

        t0 = time.time()
        while GPIO.input(config.CLIFF_ECHO) == 0:
            if time.time() - t0 > 0.03:
                return 999.0  # Timeout — treat as no obstacle

        start = time.time()
        while GPIO.input(config.CLIFF_ECHO) == 1:
            if time.time() - start > 0.03:
                return 999.0

        return (time.time() - start) * 17150.0  # cm

    def _loop(self):
        """Poll the sensor every 100ms in the background."""
        while True:
            d = self._read_cm()
            self._last_drop = d > config.CLIFF_DROP_CM
            time.sleep(0.1)

    def drop_ahead(self):
        """True if a downward drop has been detected."""
        return self._last_drop

    @staticmethod
    def upward_stair_in_scan(lidar_scan, fwd_arc_deg=30, near_m=0.6):
        """
        Heuristic upward stair detection from LiDAR.
        Returns True if there's a dense cluster of returns directly ahead
        within near_m — likely a step riser or wall.
        """
        half    = fwd_arc_deg / 2
        forward = [
            d for a, d in lidar_scan
            if (a < half or a > 360 - half) and d < near_m
        ]
        return len(forward) > 5
