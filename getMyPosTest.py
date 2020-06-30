import rospy
from turtlesim.msg import Pose
from std_msgs.msg import String
from geometry_msgs.msg import Twist

myX = 0.0
myY = 0.0
myTheta = 0.0


def nodes():
        rospy.init_node('readPOS', anonymous=True)
        getSelfPose = rospy.Subscriber('turtle1/pose', Pose, getMyPose)
        
def getMyPose(myPose):
    global myX, myY, myTheta
    myX = myPose.x
    myY= myPose.y
    myTheta = myPose.theta

def checkPose():
    pub = rospy.Publisher('myPOS', String, queue_size=10)
    rate = rospy.Rate(1) #1 hz
    while not rospy.is_shutdown():
        output = "X Coord: "+str(myX)+" Y Coord: "+str(myY)+" Theta Orentation: "+str(myTheta)
        rospy.loginfo(output)
        pub.publish(output)
        rate.sleep()

if __name__ == '__main__':
    try:
        nodes()
        checkPose()
    except rospy.ROSInterruptException:
        pass
