import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    urdf_file_name = "urdf/ur5e.urdf"
    urdf = os.path.join(
        get_package_share_directory("mc_ur5e_description"), urdf_file_name
    )

    with open(urdf, "r") as infp:
        robot_desc = infp.read()

    return LaunchDescription(
        [
            DeclareLaunchArgument("convexes", default_value="false"),
            DeclareLaunchArgument("surfaces", default_value="false"),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="both",
                parameters=[{"robot_description": robot_desc}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=[
                    "-d",
                    PathJoinSubstitution(
                        [
                            FindPackageShare("mc_ur5e_description"),
                            "rviz",
                            "view_robot2.rviz",
                        ]
                    ),
                ],
            ),
        ]
    )
