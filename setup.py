from setuptools import setup
import os
from glob import glob

package_name = 'freenove_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='thomas',
    maintainer_email='thomas@example.com',
    description='ROS 2 package for Freenove 4WD Smart Car Kit',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_node = freenove_ros2.motor_node:main',
            'servo_node = freenove_ros2.servo_node:main',
            'ultrasonic_node = freenove_ros2.ultrasonic_node:main',
            'line_tracker_node = freenove_ros2.line_tracker_node:main',
            'led_node = freenove_ros2.led_node:main',
        ],
    },
)
