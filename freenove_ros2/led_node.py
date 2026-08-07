import rclpy
from rclpy.node import Node
from std_msgs.msg import ColorRGBA
import os

class LEDNode(Node):
    """
    ROS 2 Node for WS2812 RGB LEDs.
    Note: Standard WS2812 libraries usually require root or specific 
    PWM/SPI configurations. This node provides the interface.
    """
    def __init__(self):
        super().__init__('led_node')
        self.subscription = self.create_subscription(
            ColorRGBA,
            '/led_color',
            self.color_callback,
            10)
        self.get_logger().info("LED node initialized. Waiting for commands...")

    def color_callback(self, msg):
        r, g, b = int(msg.r * 255), int(msg.g * 255), int(msg.b * 255)
        self.get_logger().info(f"Setting LED color to: R:{r} G:{g} B:{b}")
        # Integration with rpi_ws281x or similar goes here

def main(args=None):
    rclpy.init(args=args)
    node = LEDNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
