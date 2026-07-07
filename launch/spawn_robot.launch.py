import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    urdf_path           = os.path.join(get_package_share_directory('msd700_robot_description'), 'urdf', 'msd700_blade_description.urdf.xacro')
    gazebo_config_path  = os.path.join(get_package_share_directory('core_simulation'), 'config', 'gazebo_bridge.yaml')
    use_sim_time        = LaunchConfiguration('use_sim_time')

    declare_args = [
        DeclareLaunchArgument('urdf_path', default_value=urdf_path),
        DeclareLaunchArgument('gazebo_config_path', default_value=gazebo_config_path),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
    ]

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path]),
            'use_sim_time': use_sim_time,
        }]
    )

    spawn_robot_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-x', '10', '-y', '0', '-z', '2']
    )

    parameter_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_config_path}]
    )

    return LaunchDescription(
        declare_args + [
        robot_state_publisher_node,
        spawn_robot_node,
        parameter_bridge_node,
    ])