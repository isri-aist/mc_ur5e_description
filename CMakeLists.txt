cmake_minimum_required(VERSION 3.5)
project(mc_ur5e_description)

if(NOT DEFINED ENV{ROS_VERSION})
  message(FATAL_ERROR "ROS_VERSION is not set in the environment")
endif()
if($ENV{ROS_VERSION} EQUAL 1)
  set(ROS_VERSION 1)
  find_package(catkin REQUIRED COMPONENTS ur_description)
elseif($ENV{ROS_VERSION} EQUAL 2)
  set(ROS_VERSION 2)
  find_package(ament_cmake REQUIRED)
  find_package(ur_description REQUIRED)
else()
  message(FATAL_ERROR "Unknown ROS version: $ENV{ROS_VERSION}")
endif()

set(PACKAGE_NAME "ur_description")

message(STATUS "ur_description path ${ur_description_DIR}")

if("${ur_description_INSTALL_PREFIX}" STREQUAL "")
  if("${ur_description_SOURCE_PREFIX}" STREQUAL "")
    if("${ur_description_DIR}" STREQUAL "")
      message(
        FATAL_ERROR
          "ur_description does not provide SOURCE_PREFIX or INSTALL_PREFIX")
    else()
      set(ur_description_PREFIX "${ur_description_DIR}/..")
    endif()
  else()
    set(ur_description_PREFIX "${ur_description_SOURCE_PREFIX}")
  endif()
else()
  set(ur_description_PREFIX
      "${ur_description_INSTALL_PREFIX}/share/ur_description")
endif()

set(DATA_INSTALL_FOLDER "${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}")

set(xacro_SRC
    ${ur_description_PREFIX}/urdf/inc/ur_common.xacro
    ${ur_description_PREFIX}/urdf/inc/ur_transmissions.xacro
    ${ur_description_PREFIX}/config/ur5e/joint_limits.yaml
    ${ur_description_PREFIX}/config/ur5e/default_kinematics.yaml
    ${ur_description_PREFIX}/config/ur5e/physical_parameters.yaml
    ${ur_description_PREFIX}/config/ur5e/visual_parameters.yaml)

find_program(XACRO xacro REQUIRED)
set(urdf_OUT "${CMAKE_CURRENT_SOURCE_DIR}/urdf/ur5e.urdf")

if(${ROS_VERSION} EQUAL 1)
  set(xacro_IN ${ur_description_PREFIX}/urdf/ur5e.xacro)
  set(xacro_SRC ${xacro_SRC} ${xacro_IN}
                ${ur_description_PREFIX}/urdf/inc/ur_macro.xacro)

  add_custom_command(
    OUTPUT ${urdf_OUT}
    COMMAND ${XACRO} -i ${xacro_IN} -o ${urdf_OUT}
    DEPENDS ${xacro_SRC}
    COMMENT "Generate ${urdf_OUT}")
elseif(${ROS_VERSION} EQUAL 2)
  set(xacro_IN ${ur_description_PREFIX}/urdf/ur.urdf.xacro)
  set(xacro_SRC ${xacro_SRC} ${xacro_IN}
                ${ur_description_PREFIX}/urdf/ur_macro.xacro)

  add_custom_command(
    OUTPUT ${urdf_OUT}
    COMMAND ${XACRO} ${xacro_IN} name:=ur ur_type:=ur5e -o ${urdf_OUT}
    DEPENDS ${xacro_SRC}
    COMMENT "Generate ${urdf_OUT}")
endif()

add_custom_target(generate-mc-ur5e-urdf ALL DEPENDS ${urdf_OUT})
install(FILES "${urdf_OUT}" DESTINATION ${DATA_INSTALL_FOLDER}/urdf/)

install(DIRECTORY convex rsdf launch DESTINATION ${DATA_INSTALL_FOLDER})

if(${ROS_VERSION} EQUAL 1)
  catkin_package()
elseif(${ROS_VERSION} EQUAL 2)
  set(CATKIN_PACKAGE_SHARE_DESTINATION share/${PROJECT_NAME})
else()
  set(CATKIN_PACKAGE_SHARE_DESTINATION share/mc_rtc/${PROJECT_NAME})

  include(CMakePackageConfigHelpers)
  set(VERSION_CONFIG
      "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
  set(PROJECT_CONFIG "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake")
  set(CONFIG_INSTALL_DIR "lib/cmake/${PROJECT_NAME}")

  configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/ConfigVersion.cmake.in"
                 "${VERSION_CONFIG}" @ONLY)
  configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in" "${PROJECT_CONFIG}"
    INSTALL_DESTINATION "${CONFIG_INSTALL_DIR}")

  install(FILES "${VERSION_CONFIG}" "${PROJECT_CONFIG}"
          DESTINATION "${CONFIG_INSTALL_DIR}")
  install(FILES package.xml DESTINATION "${CATKIN_PACKAGE_SHARE_DESTINATION}")
endif()

foreach(dir convex launch meshes rsdf urdf rviz)
  if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${dir})
    install(DIRECTORY ${dir}/
            DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
  endif()
endforeach(dir)

if(${ROS_VERSION} EQUAL 2)
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/robot_INSTALL_PREFIX.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake/mc_ur5_description_INSTALL_PREFIX.cmake"
    @ONLY)
  ament_package(
    CONFIG_EXTRAS
    "${CMAKE_CURRENT_BINARY_DIR}/cmake/mc_ur5_description_INSTALL_PREFIX.cmake")
endif()
