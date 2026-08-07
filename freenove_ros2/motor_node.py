import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import smbus
import time

class MotorNode(Node):
    """
    ROS 2 Node to control Freenove 4WD motors via PCA9685 I2C driver.
    Converts Twist messages to PWM signals.
    """
    def __init__(self):
        super().__init__('motor_node')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        
        # PCA9685 default address 0x40
        self.address = 0x40
        try:
            self.bus = smbus.SMBus(1)
            self.init_pca9685()
            self.get_logger().info("Motor node initialized successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize PCA9685: {e}")

    def init_pca9685(self):
        self.bus.write_byte_data(self.address, 0x00, 0x00) # Mode 1
        time.sleep(0.01)

    def set_pwm(self, channel, on, off):
        self.bus.write_byte_data(self.address, 0x06 + 4 * channel, on & 0xFF)
        self.bus.write_byte_data(self.address, 0x07 + 4 * channel, on >> 8)
        self.bus.write_byte_data(self.address, 0x08 + 4 * channel, off & 0xFF)
        self.bus.write_byte_data(self.address, 0x09 + 4 * channel, off >> 8)

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z
        
        # Differential drive steering
        left_speed = linear - angular
        right_speed = linear + angular
        
        # Scale to 0-4095 range (12-bit PWM)
        # Note: Actual motor logic requires H-Bridge direction pins which usually 
        # map to specific PWM channels on the Freenove board
        self.get_logger().debug(f"Linear: {linear}, Angular: {angular} -> L: {left_speed}, R: {right_speed}")
        # Implementation depends on Freenove board wiring

def main(args=None):
    rclpy.init(args=args)
    node = MotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
