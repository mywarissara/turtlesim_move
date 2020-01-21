#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
pi = 3.14159265358979323846 
position_x = 0
position_y = 0
position_z = 0
angular_vel = 0.8 # adjust

def poseReceived(position_data): #callback
    global position_x, position_y,position_z  # When we want to change global variable from function
    position_x = position_data.x
    position_y = position_data.y
    position_z = position_data.theta

# Main program
def main():
    rospy.init_node('myrobot', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    position_publisher = rospy.Publisher('/turtle1/pose' , Pose, queue_size=10)
    pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseReceived)
    pose_msg = Pose()
    vel_msg = Twist()
    t0 = time.time()    # Get time
    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        t = time.time()
        if t >= (t0+((2*pi)/angular_vel)) and t < (t0+(2*((2*pi)/angular_vel))):
            vel_msg.angular.z = -angular_vel
            vel_msg.linear.x = 1
        elif t < t0+((2*pi)/angular_vel):
            vel_msg.angular.z = angular_vel
            vel_msg.linear.x = 1
        else:
            t0 =time.time()
        velocity_publisher.publish(vel_msg)
        print('x='+str(position_x)+'y='+str(position_y)+'theta='+str(position_z))
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass

