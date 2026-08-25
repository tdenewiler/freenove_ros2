import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import smbus
import time
import math

class MotorNode(Node):
    """
    ROS 2 Node to control Freenove 4WD motors via PCA9685 I2C driver.
    """
    def __init__(self):
        super().__init__('motor_node')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        
        self.address = 0x40
        try:
            self.bus = smbus.SMBus(1)
            self.init_pca9685()
            self.get_logger().info("Motor node initialized successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize PCA9685: {e}")

    def init_pca9685(self):
        self.write_reg(0x00, 0x00) # MODE1
        self.set_pwm_freq(50)
        time.sleep(0.01)

    def write_reg(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def read_reg(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def set_pwm_freq(self, freq):
        prescaleval = 25000000.0 / 4096.0 / float(freq) - 1.0
        prescale = math.floor(prescaleval + 0.5)
        oldmode = self.read_reg(0x00)
        self.write_reg(0x00, (oldmode & 0x7F) | 0x10)
        self.write_reg(0xFE, int(prescale))
        self.write_reg(0x00, oldmode)
        time.sleep(0.005)
        self.write_reg(0x00, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        self.write_reg(0x06 + 4 * channel, on & 0xFF)
        self.write_reg(0x07 + 4 * channel, on >> 8)
        self.write_reg(0x08 + 4 * channel, off & 0xFF)
        self.write_reg(0x09 + 4 * channel, off >> 8)

    def move_wheel(self, channels, duty):
        ch_a, ch_b = channels
        if duty > 0:
            self.set_pwm(ch_a, 0, 0)
            self.set_pwm(ch_b, 0, duty)
        elif duty < 0:
            self.set_pwm(ch_b, 0, 0)
            self.set_pwm(ch_a, 0, abs(duty))
        else:
            self.set_pwm(ch_a, 0, 4095)
            self.set_pwm(ch_b, 0, 4095)

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z
        
        left_speed = linear - angular
        right_speed = linear + angular
        
        left_duty = int(left_speed * 4095)
        right_duty = int(right_speed * 4095)
        
        left_duty = max(min(left_duty, 4095), -4095)
        right_duty = max(min(right_duty, 4095), -4095)

        # Freenove 4WD Mapping
        self.move_wheel((0, 1), left_duty)   # LU
        self.move_wheel((3, 2), left_duty)   # LL
        self.move_wheel((6, 7), right_duty)  # RU
        self.move_wheel((4, 5), right_duty)  # RL

def main(args=None):
    rclpy.init(args=args)
    node = MotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop motors
        for i in range(8):
            node.set_pwm(i, 0, 0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
