import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    world_path          = os.path.join(get_package_share_directory('core_simulation'), 'world/tugbot_depot/tugbot_depot.sdf')
    # world_path          = os.path.join(get_package_share_directory('core_simulation'), 'world/sandy_world/sandy_world.sdf')
    # world_path          = os.path.join(get_package_share_directory('core_simulation'), 'world/empty_world.world')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items()
    )


    return LaunchDescription([
        gz_sim,
    ])