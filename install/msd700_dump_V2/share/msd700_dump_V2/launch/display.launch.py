"""Display an MSD700 robot description in RViz 2.

Examples:
  ros2 launch msd700_dump_V2 display.launch.py model:=model_4
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import xacro

# model name -> (xacro file relative to urdf/, root frame for RViz)
MODELS = {
    'model_1': ('model_1/msd700_blade_description.urdf.xacro', 'base_footprint'),
    'model_2': ('model_2/msd700_prototype_mid.urdf.xacro', 'base_footprint'),
    'model_3': ('model_3/msd700_prototype.urdf.xacro', 'base_link'),
    'model_4': ('model_4/msd700_dump_description.urdf.xacro', 'base_footprint'),
}


def launch_setup(context):
    pkg_share = get_package_share_directory('msd700_dump_V2')
    model = LaunchConfiguration('model').perform(context)
    if model not in MODELS:
        raise RuntimeError(f"Unknown model '{model}', choose one of {list(MODELS)}")
    xacro_rel, fixed_frame = MODELS[model]

    mappings = {}
    if model in ('model_2', 'model_3'):
        mappings['config_file'] = LaunchConfiguration('config_file').perform(context)

    robot_description = xacro.process_file(
        os.path.join(pkg_share, 'urdf', xacro_rel), mappings=mappings).toxml()

    use_gui = LaunchConfiguration('gui').perform(context).lower() == 'true'

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': ParameterValue(robot_description, value_type=str)}],
        ),
        Node(
            package='joint_state_publisher_gui' if use_gui else 'joint_state_publisher',
            executable='joint_state_publisher_gui' if use_gui else 'joint_state_publisher',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(pkg_share, 'config', 'rviz', 'display.rviz'),
                       '-f', fixed_frame],
        ),
    ]


def generate_launch_description():
    pkg_share = get_package_share_directory('msd700_dump_V2')
    return LaunchDescription([
        DeclareLaunchArgument('model', default_value='model_1',
                              description='model_1 | model_2 | model_3 | model_4'),
        DeclareLaunchArgument('config_file',
                              default_value=os.path.join(pkg_share, 'config', 'msd700_xacro_config.yaml'),
                              description='model_2/model_3 only: dimensions yaml'),
        DeclareLaunchArgument('gui', default_value='true',
                              description='Show joint_state_publisher_gui sliders'),
        OpaqueFunction(function=launch_setup),
    ])
