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

chaseX = 0.0
chaseY = 0.0
chaseTheta = 0.0

chase2X = 0.0
chase2Y = 0.0
chase2Theta = 0.0

def createGoalTurtle():
    global goalX, goalY, goalTheta
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')

def createChaseTurtle():
    chaseTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    chaseTurtle(0,0,0,'chaseTurtle')

def createSecondChaseTurtle():
    chaseTurtleTwo = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    chaseTurtleTwo(5,0,0,'chaseTurtle2')

def removeGoalTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

def removeChaseTurtle():
    chaseTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    chaseTurtle('chaseTurtle')

def removeChase2Turtle():
    chase2Turtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    chase2Turtle('chase2Turtle')

def getMyPos(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta

def getChasePos(chasePos):
    global chaseX, chaseY, chaseTheta
    chaseX = chasePos.x
    chaseY = chasePos.y
    chaseTheta = chasePos.theta

def get2ChasePos(chase2Pos):
    global chase2X, chase2Y, chase2Theta
    chase2X = chase2Pos.x
    chase2Y = chase2Pos.y
    chase2Theta = chase2Pos.theta

def velocity():
    myVel = Twist()
    chaseVel = Twist()
    chase2Vel = Twist()
    while not rospy.is_shutdown():
        #set up axis
        xAxis = goalX - myX
        yAxis = goalY -myY
        xChase = myX - chaseX
        yChase = myY - chaseY
        x2Chase = chaseX - chase2X
        y2Chase = chaseY - chase2Y
        chaseAxisX = goalX - chase2X
        chaseAxisY = goalY - chase2Y
        #set up distances
        distance = abs(((xAxis**2) + (yAxis**2))**.5)
        chaseDistance = abs(((xChase**2) + (yChase**2))**.5)
        chase2Distance = abs(((x2Chase**2) + (y2Chase**2))**.5)
        distanceChase2andTurtle1 = abs(((chaseAxisX**2) + (chaseAxisY**2))**.5)
        #setUp angles
        relativeAngle = (math.atan2(yAxis, xAxis)-myTheta)
        chaseAngle = (math.atan2(yChase, xChase)-chaseTheta)
        chase2Angle = (math.atan2(y2Chase, x2Chase)-chase2Theta)
        #turtle1/
        if(-.05 > relativeAngle or relativeAngle > .05):
            myVel.linear.x = distance / 10
            myVel.angular.z = relativeAngle * 4
            if(abs(relativeAngle) > math.pi):
                myVel.angular.z = (math.pi - relativeAngle) * 4
            setVelocity.publish(myVel)
        if((-.05 < relativeAngle and relativeAngle < .05)):
            myVel.linear.x = distance * 2
            setVelocity.publish(myVel)
        if(distance < .3):
            distance = 100
            removeGoalTurtle()
            createGoalTurtle()
        #turtle2
        chaseVel.linear.x = chaseDistance / 4
        chaseVel.angular.z = chaseAngle * 4
        setChaseVelocity.publish(chaseVel)
        if(chaseDistance < 1):
            chaseVel.linear.x *= -10
            chaseVel.angular.z = -chaseAngle
            setChaseVelocity.publish(chaseVel)
        #turtle3
        chase2Vel.linear.x = chase2Distance / 8
        chase2Vel.angular.z = chase2Angle * 4
        set2ChaseVelocity.publish(chase2Vel)
        if(chase2Distance < 1):
            chase2Vel.linear.x *=-10
            chase2Vel.angular.z = -chase2Angle
            set2ChaseVelocity.publish(chase2Vel)
        if(distanceChase2andTurtle1 < 1):
            chase2Vel.linear.x *=-10
            chase2Vel.angular.z = -chase2Angle
            set2ChaseVelocity.publish(chase2Vel)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('chaseTurtleV1', anonymous=False)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPos)
        chasePose = rospy.Subscriber('chaseTurtle/pose', Pose, getChasePos)
        secondChasePose = rospy.Subscriber('chaseTurtle2/pose', Pose, get2ChasePos)
        setVelocity = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        setChaseVelocity = rospy.Publisher('chaseTurtle/cmd_vel', Twist, queue_size = 10)
        set2ChaseVelocity = rospy.Publisher('chaseTurtle2/cmd_vel', Twist, queue_size = 10)
        rate = rospy.Rate(100)
        createGoalTurtle()
        #turtle1 already exists
        createChaseTurtle()
        createSecondChaseTurtle()
        velocity()
    except rospy.ROSInterruptException:
        pass
