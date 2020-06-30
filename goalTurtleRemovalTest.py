import rospy
import turtlesim.srv

def removeTurtle():
    goalTurtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    goalTurtle('goalTurtle')

if __name__ == '__main__':
    try:
        removeTurtle()
    except rospy.ROSInterruptException:
        pass
