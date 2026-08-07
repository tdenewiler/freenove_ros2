from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='freenove_ros2', executable='motor_node', name='motor_node'),
        Node(package='freenove_ros2', executable='servo_node', name='servo_node'),
        Node(package='freenove_ros2', executable='ultrasonic_node', name='ultrasonic_node'),
        Node(package='freenove_ros2', executable='line_tracker_node', name='line_tracker_node'),
        Node(package='freenove_ros2', executable='led_node', name='led_node'),
    ])
