import rospy
import random
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import turtlesim.srv

myX = 0.0
myY = 0.0
myTheta = 0.0

goalX = None
goalY = None
goalTheta = None

def node():
    createGoalTurtle()
    rospy.init_node('goToGoalTurtle', anonymous=True)
    goalPose = rospy.Subscriber('goalTurtle/pose', Pose, getGoalPose)
    myPose = rospy.Subscriber('turtle1/pose', Pose, getMyPose)
    pub = rospy.Publisher('GoalTurtlePos', String, queue_size = 10)

def createGoalTurtle():
    global goalX, goalY, goalTheta
    goalTurtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    goalX = round(random.uniform(1,10), 3)
    goalY = round(random.uniform(1,10), 3)
    goalTheta = round(random.uniform(0,6.3), 3) #6.3 is used as an approximation of 2pi
    goalTurtle(goalX, goalY, goalTheta, 'goalTurtle')

def getGoalPose(goalPos):
    global goalX, goalY, goalTheta
    goalX = goalPos.x
    goalY= goalPos.y
    goalTheta = goalPos.theta
def getMyPose(myPos):
    global myX, myY, myTheta
    myX = myPos.x
    myY= myPos.y
    myTheta = myPos.theta
def checkGoalPose():
    pub = rospy.Publisher('GoalPOS', String, queue_size=10)
    rate = rospy.Rate(1) #1 hz
    while not rospy.is_shutdown():
        output = "X Coord: "+str(goalX)+" Y Coord: "+str(goalY)+" Theta Orentation: "+str(goalTheta)
        rospy.loginfo(output)
        pub.publish(output)
        rate.sleep()

if __name__ == '__main__':
    try:
        node()
        checkGoalPose()
    except rospy.ROSInterruptException:
        pass
