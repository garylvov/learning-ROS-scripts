import rospy
import random
import math
import turtlesim.srv
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

myX = 0.0
myY = 0.0
myTheta = 0.0

goalX = 0.0
goalY = 0.0
goalTheta = 0.0

def createGoalTurtle():
    global goalX, goalY, goalTheta
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')

def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

def getMyPose(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta

def velocity():
    createGoalTurtle()
    myVel = Twist()
    while not rospy.is_shutdown():
        xAxis = goalX - myX
        yAxis = goalY -myY
        distance = abs(((xAxis**2) + (yAxis**2))**.5)
        relativeAngle = (math.atan2(yAxis, xAxis)-myTheta)
        myVel.linear.x = distance
        myVel.angular.z = relativeAngle
        setVelocity.publish(myVel)
        if(distance < .3):
            removeTurtle()
            velocity()
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('goToGoalTurtleV1', anonymous=False)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPose)
        setVelocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        rate = rospy.Rate(1)
        velocity()
    except rospy.ROSInterruptException:
        pass
