# UR5e robot description for [mc_rtc](https://jrl-umi3218.github.io/mc_rtc/)
This package has additional convex files for mc_ur5e robot module used by [mc_rtc](https://jrl-umi3218.github.io/mc_rtc/) control framework.
UR5e robot has urdf, collada and meshes in the original [ur_description](https://github.com/ros-industrial/universal_robot/tree/melodic-devel/ur_description) package.

It contains the following directories:
- `convex/`: convex hulls (generated from pointclouds sampled from the dae meshes)
- `rsdf/`: Special urdf-like format describing surfaces attached to links on the robot (The folder is empty)

## Required dependencies

* ROS1 : [ur_description](https://github.com/ros-industrial/universal_robot/tree/melodic-devel/ur_description)
* ROS2 : [ur_description](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description)

## Installation

### ROS1 
  On an environment with ROS and catkin properly setup:

  ```bash
  $ cd ~/catkin_ws/src
  $ git clone https://github.com/ros-industrial/universal_robot
  $ git clone https://github.com/isri-aist/mc_ur5e_description
  $ cd ..
  $ catkin_make
  ```

  If you install into a different directory than the src directory of the catkin workspace, run the following commands.
  ```bash
  $ cd build
  $ make install
  ```
  If your catkin environment is sourced `source ~/catkin_ws/install/setup.bash`, the robot model will be available to all ROS tools, and mc_rtc robot module.

  To display the robot, you can use:

  ```
  $ roslaunch mc_ur5e_description display_ur5e.launch
  ```


### ROS2
  On an envrionnement with ROS and a workspace properly setup : 

  ```bash 
  $ cd ~/ros2_ws/src
  $ git clone https://github.com/UniversalRobots/Universal_Robots_ROS2_Description # you may need to change branch depending on your ros version
  $ git clone https://github.com/isri-aist/mc_ur5e_description
  $ cd ..
  $ colcon build
  ```
  If your catkin environment is sourced `source ~/ros2_ws/install/setup.bash`, the robot model will be available to all ROS tools, and mc_rtc robot module.

  To display the robot, you can use:

  ```bash
  $ ros2 launch mc_ur5e_description display_ur5e.launch.py
  ```

> If you have mc_rtc and the corresponding robot module installed, you can use the `convexes:=True` or `surfaces:=True` arguments to display the robot convexes and surfaces. These arguments can be used for both ROS version.
***

## When updating convex files

### Dependencies
- [ur_description](https://github.com/ros-industrial/universal_robot/tree/melodic-devel/ur_description)
- [mesh_sampling](https://github.com/arntanguy/mesh_sampling)
- qhull-bin

### Generation of convex files
To run the conversion, simply run

```
$ source ~/catkin_ws/devel/setup.bash
$ roscd mc_ur5e_description/scripts
$ ./generate_convex.sh
  Running generate_convex.sh script from directory <MC_UR5E_DESCRIPTION_PATH>/script
      :
      :
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/upperarm.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/forearm.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/base.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/wrist2.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/wrist3.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/shoulder.stl
  -- Generating convex hull for /home/@USERNAME@/catkin_ws/install/share/ur_description/meshes/ur5e/collision/wrist1.stl

  Successfully generated convex from ur_description package in /tmp/mc_ur5e_description

$ mv /tmp/mc_ur5e_description/convex/ur5e `rospack find mc_ur5e_description`/convex/
```
