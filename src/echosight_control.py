#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import math

class EchoSightControl(Node):
    def __init__(self):
        super().__init__('echosight_control')
        self.subscription = self.create_subscription(LaserScan, '/filtered_scan', self.scan_callback, 10)
        self.alert_pub = self.create_publisher(String, '/echosight/alerts', 10)
        
        self.STOP_DIST = 0.35  # Sensitive trigger for low objects
        self.get_logger().info("EchoSight Control: Sensitive Mode Active.")

    def scan_callback(self, msg):
        if not msg.ranges: return
        
        n = len(msg.ranges)
        # Look at the front 20% of the field of view
        front_sector = msg.ranges[int(n*0.4):int(n*0.6)]
        
        # Filter out 'inf' (nothing) and 'nan' so we only see solid objects
        valid_front = [d for d in front_sector if not math.isinf(d) and not math.isnan(d)]
        
        # Get the closest object in the front sector
        min_front = min(valid_front) if valid_front else 10.0
        
        msg_out = String()
        
        # Logic: If anything is closer than 0.35m, stop immediately
        if min_front < self.STOP_DIST:
            msg_out.data = "STOP"
        else:
            msg_out.data = "PATH CLEAR"
            
        self.alert_pub.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = EchoSightControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
