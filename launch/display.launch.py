import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # rviz_config_path    = os.path.join(get_package_share_directory('core_mapping'), 'rviz', 'slam_toolbox.rviz')
    # rviz_config_path    = os.path.join(get_package_share_directory('core_mapping'), 'rviz', 'glim_ros.rviz')
    # rviz_config_path    = os.path.join(get_package_share_directory('core_localization'), 'rviz', 'glim_odometry_ros.rviz')
    rviz_config_path    = os.path.join(get_package_share_directory('core_navigation'), 'rviz', 'nav2_default_view.rviz')
    # rviz_config_path    = os.path.join(get_package_share_directory('core_simulation'), 'rviz', 'msd700_blade.rviz')
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    joint_pub_arg = LaunchConfiguration('joint_pub')

    declare_args = [
        DeclareLaunchArgument('use_sim_time',default_value='false'),
        DeclareLaunchArgument('joint_pub', default_value='true'),
    ]

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(joint_pub_arg)
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription(
        declare_args + [
        joint_state_publisher_gui_node,
        rviz_node,
        ]
    )