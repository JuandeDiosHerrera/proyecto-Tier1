cmake_minimum_required(VERSION 2.8.3)
project(bateria)

find_package(catkin REQUIRED COMPONENTS
  diagnostic_msgs
  roscpp
  std_msgs
  actionlib
  kobuki_msgs
  sos
  geometry_msgs
  std_srvs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bateria
  CATKIN_DEPENDS 
  diagnostic_msgs 
  roscpp 
  std_msgs
  actionlib
  kobuki_msgs
  geometry_msgs
  std_srvs
#  DEPENDS system_lib
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(control_bateria_autodocking src/control_bateria.cpp)
add_executable(autodocking src/autodocking.cpp)

target_link_libraries(control_bateria_autodocking ${catkin_LIBRARIES})
target_link_libraries(autodocking ${catkin_LIBRARIES})


