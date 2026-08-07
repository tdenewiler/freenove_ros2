import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO
import time

class UltrasonicNode(Node):
    """
    ROS 2 Node for HC-SR04 ultrasonic sensor.
    Publishes Range messages at 10Hz.
    """
    def __init__(self):
        super().__init__('ultrasonic_node')
        self.publisher_ = self.create_publisher(Range, '/ultrasonic/range', 10)
        self.timer = self.create_timer(0.1, self.measure_distance)
        
        # Freenove default pins for HC-SR04
        self.TRIG = 11 # GPIO 17
        self.ECHO = 12 # GPIO 18
        
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.TRIG, GPIO.OUT)
            GPIO.setup(self.ECHO, GPIO.IN)
            self.get_logger().info("Ultrasonic node initialized")
        except Exception as e:
            self.get_logger().error(f"GPIO Init Error: {e}")

    def measure_distance(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        
        pulse_start = time.time()
        pulse_end = time.time()
        
        # Wait for echo
        start_timeout = time.time()
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
            if pulse_start - start_timeout > 0.1: return

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()
            if pulse_end - pulse_start > 0.1: return
            
        duration = pulse_end - pulse_start
        distance = duration * 17150 # Speed of sound / 2
        
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "ultrasonic_link"
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.52 # Approx 30 deg
        msg.min_range = 0.02
        msg.max_range = 4.0
        msg.range = float(distance / 100.0)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
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
