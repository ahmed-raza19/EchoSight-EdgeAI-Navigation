#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarFilterNode(Node):
    def __init__(self):
        super().__init__('lidar_filter_node')
        # Subscribes to raw RPLiDAR data
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        # Publishes the clean data used by control logic
        self.publisher = self.create_publisher(LaserScan, '/filtered_scan', 10)
        self.get_logger().info("LiDAR Filter Node: Processing raw data...")

    def scan_callback(self, msg):
        # We pass the data through to /filtered_scan
        # Add filtering logic here if you need to cap max distance
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
