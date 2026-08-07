import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import RPi.GPIO as GPIO

class LineTrackerNode(Node):
    """
    ROS 2 Node for 3-channel infrared line tracker.
    """
    def __init__(self):
        super().__init__('line_tracker_node')
        self.publisher_ = self.create_publisher(Int32MultiArray, '/line_tracker/raw', 10)
        self.timer = self.create_timer(0.1, self.read_sensors)
        
        # Freenove default pins
        self.pins = [13, 15, 16] # GPIO 27, 22, 23
        
        try:
            GPIO.setmode(GPIO.BOARD)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.IN)
            self.get_logger().info("Line tracker node initialized")
        except Exception as e:
            self.get_logger().error(f"GPIO Init Error: {e}")

    def read_sensors(self):
        msg = Int32MultiArray()
        msg.data = [GPIO.input(pin) for pin in self.pins]
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LineTrackerNode()
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
