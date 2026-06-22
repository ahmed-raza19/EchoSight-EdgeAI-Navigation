# tests/test_lidar.py
from rplidar import RPLidar
import time

PORT = '/dev/ttyUSB0'

lidar = RPLidar(PORT, baudrate=115200, timeout=3)

try:
    print('Info   :', lidar.get_info())
    print('Health :', lidar.get_health())
    print('\nScanning... (Ctrl-C to stop)\n')

    for i, scan in enumerate(lidar.iter_scans(min_len=50)):
        closest = min(p[2] for p in scan)
        print(f'Scan {i:03d} | {len(scan):3d} points | closest = {closest:.0f} mm')
        if i >= 9:
            break

finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    print('\nStopped.')
