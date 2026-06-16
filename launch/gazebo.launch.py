import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    urdf_path           = os.path.join(get_package_share_directory('msd700_robot_description'), 'urdf', 'msd700_blade_description.urdf.xacro')
    rviz_config_path    = os.path.join(get_package_share_directory('msd700_robot_description'), 'rviz', 'msd700_blade.rviz')
    gazebo_config_path  = os.path.join(get_package_share_directory('msd700_robot_description'), 'config', 'gazebo_bridge.yaml')
    world_path          = os.path.join(get_package_share_directory('msd700_robot_description'), 'world', 'sandy_world.sdf')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path])
        }]
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': world_path}.items()
    )
    
    spawn_robot_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-x', '200', '-y', '200', '-z', '10']
    )

    parameter_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_config_path}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    ld = LaunchDescription()

    ld.add_action(robot_state_publisher_node)
    ld.add_action(gz_sim)
    ld.add_action(spawn_robot_node)
    ld.add_action(parameter_bridge_node)
    ld.add_action(rviz_node)
    
    return ld