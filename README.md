# freenove_ros2

ROS 2 package for Freenove 4WD Smart Car Kit for Raspberry Pi.

## Nodes

- `motor_node`: Controls the 4WD motors via PCA9685. Subscribes to `/cmd_vel`.
- `servo_node`: Controls the pan-tilt servos via PCA9685. Subscribes to `/pan_tilt_angles`.
- `ultrasonic_node`: Measures distance via HC-SR04. Publishes to `/ultrasonic/range`.
- `line_tracker_node`: Reads the 3-channel infrared line tracker. Publishes to `/line_tracker/raw`.
- `led_node`: Controls the onboard WS2812 LEDs. Subscribes to `/led_color`.

## Hardware Setup

Ensure I2C is enabled on the Raspberry Pi.
To run without root, ensure the user is in `i2c`, `gpio` and `video` groups.
