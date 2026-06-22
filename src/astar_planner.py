# astar_planner.py
import heapq, math
import numpy as np
import config

class AStarPlanner:
    """
    Custom A* pathfinder on a 2D occupancy grid built from LiDAR scans.

    Coordinate frame: x = forward, y = left (meters, car-relative).
    The car always sits at the grid origin. Grid is rebuilt each scan.
    Obstacles are inflated by the robot's physical radius before planning.
    """

    def __init__(self):
        self.res    = config.GRID_RES_M
        n           = int(config.GRID_SIZE_M / self.res)
        self.n      = n
        self.grid   = np.zeros((n, n), dtype=np.uint8)  # 0=free, 1=obstacle
        self.origin = (n // 2, n // 2)                  # car at center

    # ── Coordinate conversion ──────────────────────────────────────────────

    def world_to_grid(self, x, y):
        cx, cy = self.origin
        gx = cx + int(round(x / self.res))
        gy = cy + int(round(y / self.res))
        return gx, gy

    def grid_to_world(self, gx, gy):
        cx, cy = self.origin
        return (gx - cx) * self.res, (gy - cy) * self.res

    # ── Grid update ────────────────────────────────────────────────────────

    def update_from_scan(self, lidar_xy):
        """
        Rebuild the occupancy grid from the latest LiDAR (x, y) points.
        lidar_xy: list of (x, y) tuples in metres, car-frame.
        """
        self.grid.fill(0)

        for x, y in lidar_xy:
            gx, gy = self.world_to_grid(x, y)
            if 0 <= gx < self.n and 0 <= gy < self.n:
                self.grid[gx, gy] = 1

        # Inflate obstacles so the rover body doesn't clip corners
        if config.INFLATE_CELLS > 0:
            from scipy.ndimage import binary_dilation
            self.grid = binary_dilation(
                self.grid, iterations=config.INFLATE_CELLS
            ).astype(np.uint8)

    # ── A* search ─────────────────────────────────────────────────────────

    def plan(self, start_world, goal_world):
        """
        Find a path from start to goal in world coordinates (metres).
        Returns list of (x, y) waypoints, or [] if no path exists.
        """
        sx, sy = self.world_to_grid(*start_world)
        gx, gy = self.world_to_grid(*goal_world)

        if not self._free(sx, sy) or not self._free(gx, gy):
            return []

        def h(a, b):
            return math.hypot(a[0] - b[0], a[1] - b[1])

        open_set = [(0, (sx, sy))]
        came     = {(sx, sy): None}
        g_score  = {(sx, sy): 0.0}

        while open_set:
            _, cur = heapq.heappop(open_set)

            if cur == (gx, gy):
                return self._reconstruct(came, cur)

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nb = (cur[0] + dx, cur[1] + dy)
                    if not self._free(*nb):
                        continue
                    step_cost = math.hypot(dx, dy)
                    tg = g_score[cur] + step_cost
                    if tg < g_score.get(nb, float('inf')):
                        came[nb]    = cur
                        g_score[nb] = tg
                        f           = tg + h(nb, (gx, gy))
                        heapq.heappush(open_set, (f, nb))

        return []  # No path found

    # ── Helpers ───────────────────────────────────────────────────────────

    def _free(self, gx, gy):
        return (0 <= gx < self.n and 0 <= gy < self.n
                and self.grid[gx, gy] == 0)

    def _reconstruct(self, came, end):
        path, cur = [], end
        while cur is not None:
            path.append(self.grid_to_world(*cur))
            cur = came[cur]
        return path[::-1]
