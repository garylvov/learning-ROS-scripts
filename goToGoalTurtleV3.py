#This code has a mild bug:
#When traveling left horizontally turtle is erratic
import rospy
import random
import math
import time
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
    global goalX, goalY
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')

def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

def getMyPos(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta

def velocity():
    myVel = Twist()
    myVel.linear.x = 0
    myVel.angular.y = 0
    setVelocity.publish(myVel)
    while not rospy.is_shutdown():
        xAxis = goalX - myX
        yAxis = goalY - myY
        distance = abs(((xAxis**2) + (yAxis**2))**.5)
        relativeAngle = (math.atan2(yAxis, xAxis)-myTheta)
        if(-.05 > relativeAngle or relativeAngle > .05):
            myVel.linear.x = distance / 4
            myVel.angular.z = relativeAngle * 5
            if(abs(relativeAngle) > math.pi):
                myVel.angular.z = (math.pi - relativeAngle) * 5
            setVelocity.publish(myVel)
        myVel.angular.z = 0
        if((-.05 < relativeAngle and relativeAngle < .05)):
            myVel.linear.x = distance * 4
            setVelocity.publish(myVel)
        if(distance < .4):
            removeTurtle()
            createGoalTurtle()

if __name__ == '__main__':
    try:
        createGoalTurtle()
        rospy.init_node('goToGoalTurtleV3', anonymous=False)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPos)
        setVelocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        rate = rospy.Rate(10)
        velocity()
    except rospy.ROSInterruptException:
        pass
