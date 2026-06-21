#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO

class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')
        self.subscription = self.create_subscription(String, '/echosight/alerts', self.alert_callback, 10)
        
        # GPIO Setup
        self.LEFT_PIN = 17
        self.RIGHT_PIN = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_PIN, GPIO.OUT)
        
        self.get_logger().info("Motor Driver: Ready and awaiting alerts.")

    def alert_callback(self, msg):
        if msg.data == "STOP":
            GPIO.output(self.LEFT_PIN, GPIO.LOW)
            GPIO.output(self.RIGHT_PIN, GPIO.LOW)
            self.get_logger().warn("Obstacle detected! Motors stopped.")
        else:
            GPIO.output(self.LEFT_PIN, GPIO.HIGH)
            GPIO.output(self.RIGHT_PIN, GPIO.HIGH)
            self.get_logger().info("Path clear. Motors running.")

def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
