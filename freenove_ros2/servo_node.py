import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import smbus

class ServoNode(Node):
    """
    ROS 2 Node to control Pan-Tilt servos via PCA9685.
    Subscribes to /pan_tilt_angles [pan, tilt] in degrees.
    """
    def __init__(self):
        super().__init__('servo_node')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/pan_tilt_angles',
            self.angle_callback,
            10)
        
        self.address = 0x40
        try:
            self.bus = smbus.SMBus(1)
            self.get_logger().info("Servo node initialized successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize I2C: {e}")

    def angle_callback(self, msg):
        if len(msg.data) >= 2:
            pan = msg.data[0]
            tilt = msg.data[1]
            self.get_logger().info(f"Setting Pan: {pan}, Tilt: {tilt}")
            # Map degrees to PWM pulses (usually 500-2500us for servos)

def main(args=None):
    rclpy.init(args=args)
    node = ServoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
