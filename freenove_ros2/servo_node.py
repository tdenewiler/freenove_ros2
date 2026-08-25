import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import smbus
import time
import math

class ServoNode(Node):
    """
    ROS 2 Node to control Pan-Tilt servos via PCA9685.
    Mapping:
    - Channel 8: Pan
    - Channel 9: Tilt
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
            self.init_pca9685()
            # Initialize servos to 90 degrees
            self.set_servo_angle(8, 90, reverse=True) # Pan
            self.set_servo_angle(9, 90, reverse=False) # Tilt
            self.get_logger().info("Servo node initialized successfully")
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

    def set_servo_pulse(self, channel, pulse):
        duty = int(pulse * 4096 / 20000)
        self.set_pwm(channel, 0, duty)

    def set_servo_angle(self, channel, angle, reverse=False):
        angle = max(0, min(180, angle))
        error = 10
        if reverse:
            pulse = 2500 - int((angle + error) / 0.09)
        else:
            pulse = 500 + int((angle + error) / 0.09)
        self.set_servo_pulse(channel, pulse)

    def angle_callback(self, msg):
        if len(msg.data) >= 2:
            pan = msg.data[0]
            tilt = msg.data[1]
            self.set_servo_angle(8, pan, reverse=True)
            self.set_servo_angle(9, tilt, reverse=False)

def main(args=None):
    rclpy.init(args=args)
    node = ServoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # To "stop" or de-energize servos, we set PWM to 0
        node.set_pwm(8, 0, 0)
        node.set_pwm(9, 0, 0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
