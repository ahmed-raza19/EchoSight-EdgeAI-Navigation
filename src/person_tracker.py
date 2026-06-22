# person_tracker.py
import math, time
import config

class PersonTracker:
    """
    Tracks the user's position using LiDAR points in the rear arc.

    The rover expects the user to walk behind it. This module clusters
    the rear LiDAR returns, finds the one that looks like a person
    (5-15 point cluster at ~0.7-1.1m), and watches their distance
    over time to detect if they've stopped.
    """

    def __init__(self):
        self.last_seen    = 0.0
        self.last_dist    = None
        self.last_bearing = None   # degrees offset from dead-rear
        self.history      = []     # (timestamp, distance) for stop detection

    def update(self, scan):
        """
        scan: list of (angle_deg, distance_m) from LidarNode.get_scan()
        Returns a dict {dist, bearing, score, n} or None if user not found.
        """
        half = config.USER_ARC_DEG / 2

        # Extract rear arc — angles near 180° (directly behind the car)
        rear = [
            (a, d) for a, d in scan
            if (180 - half) <= a <= (180 + half) and 0.3 < d < 2.0
        ]

        if not rear:
            return self._lost()

        # Simple 1D angular clustering — split on gaps > 8°
        rear.sort(key=lambda x: x[0])
        clusters, cur = [], [rear[0]]
        for prev, p in zip(rear, rear[1:]):
            if abs(p[0] - prev[0]) > 8.0:
                clusters.append(cur)
                cur = [p]
            else:
                cur.append(p)
        clusters.append(cur)

        # Score clusters: prefer those near 0.9m and with enough points
        best = None
        for cl in clusters:
            mean_d = sum(d for _, d in cl) / len(cl)
            mean_a = sum(a for a, _ in cl) / len(cl)
            score = abs(mean_d - 0.9) + 0.005 * (10 - len(cl))
            if best is None or score < best['score']:
                best = {
                    'score':   score,
                    'dist':    mean_d,
                    'bearing': mean_a - 180,  # offset from rear center
                    'n':       len(cl)
                }

        if best is None or best['n'] < 3:
            return self._lost()

        # Update state
        self.last_seen    = time.time()
        self.last_dist    = best['dist']
        self.last_bearing = best['bearing']

        # Rolling 1.5s history for stop detection
        self.history.append((self.last_seen, best['dist']))
        self.history = [(t, d) for t, d in self.history
                        if t > self.last_seen - 1.5]

        return best

    def _lost(self):
        return None

    def is_lost(self):
        """True if user hasn't been seen for USER_LOST_S seconds."""
        return (time.time() - self.last_seen) > config.USER_LOST_S

    def is_stopped(self):
        """True if user's distance has barely changed for the last ~1.5 seconds."""
        if len(self.history) < 5:
            return False
        ds = [d for _, d in self.history]
        return (max(ds) - min(ds)) < 0.05  # less than 5cm variation = stopped
