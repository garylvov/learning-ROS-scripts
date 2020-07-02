# learning-ROS-scripts

SELECT RAW FOR PROPER FORMATTING

////////////////////////////////////
/Downloading / running the scripts:/
////////////////////////////////////

1.) Have ROS installed on your computer:
  http://wiki.ros.org/noetic/Installation

2.) Create a catkin file system if you do not already have one, and add a project with dependencies on rospy, std_msgs, tf, and turtlesim.
  
  Creating a file system if you do not have one:
  mkdir -p ~/catkin_ws/src
  cd ~/catkwin_ws/src
  catkin_init_workspace
  cd ~/catkin_ws/
  catkin_make
  
  Creating a Project:
  cd ~/catkin_ws/src
  catkin_create_pkg learning_ros std_msgs rospy turtlesim tf
  cd ~/catkin_ws/
  catkin_make
  
3.) Switch to the /src/PROJECTNAME file and open up CMakeLists.txt
 
4.) Append the following (delete the names of programs that you are not going to install):

catkin_install_python(PROGRAMS
  scripts/goalTurtleCreationTest.py
  scripts/goalTurtleRemovalTest.py
  scripts/getMyPosTest.py
  scripts/goToGoalTurtleV1.py
  scripts/goToGoalTurtleV2.py
  scripts/getGoalPosTest.py
  scripts/chaseTurtleV1.py
  scripts/goToGoalTurtleV3.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

5.) Open ~/catkin_ws/src/learning_ros and create a folder called scripts
6.) Add a file for each script you plan to run in the scripts folder with it's given name, and copy the scripts contents from github into said file.

6.) Make the file executable  
  cd ~/catkin_ws/src/learning_ros/scripts
  chmod +x INSERT-FILENAME-HERE
7.) In command run the files
  roscore
  rosrun turtlesim turtlesim_node
  rosrun learing_ros INSERT-FILENAME-HERE
  
//////////////////////////////
/Information on each script /
/////////////////////////////

goalTurtleCreationTest.py:
Tests the creation of a goalTurtle in a random location and saves it's location with use of global variables

goalTurtleRemovalTest:
Tests removing a goalTurtle, goalTurtle must be spawned first using goalTurtleCreationTest.py

getMyPosTest.py:
Subscirbes to turtle1/pose and prints the position of the turtle to the console, as well as publishes that info

getGoalPosTest:
Spawns a goalturtle, subscribes to its pose, prints the position to the console, as well as publishes that info

goToGoalTurtleV1:
Spawns a turtle in a random location
Has a turtle chase the randomly spawned turtle using PID control
On collision turtle is respawned in another random location

goToGoalTurtleV2:
Spawns a turtle in a random location
Has a turtle chase the randomly spawned turtle using PID control, most efficent turns, and more efficent paths
On collision turtle is respawned in another random location

goToGoalTurtleV3
Spawns a turtle in a random location
Has a turtle chase the randomly spawned turtle using PID control, efficent turns, efficent paths, more immediate respawn of the goal turtle, and smoother animation
On collision turtle is respawned in another random location

chaseTurtleV1:
Spawns a turtle in a random location
Has a turtle chase the randomly spawned turtle using PID control, efficent turns, efficent paths, immediate respawn of the goal turtle, and smooth animation
On collision turtle is respawned in another random location
Has a turtle following the turtle that is chasing the randomly spawned turtle with PID control from goToGoalTurtle V1 with decreased speed
Has a turtle following the chase turtle with PID control from goToGoalTurtleV1 with even further decreased speed
All three turtles have collision avoidance
