import rospy
import numpy as np

import pdb
import time
import thread
import time
import math

from std_msgs.msg import Float64, Float32
from sensor_msgs.msg import JointState
from dvs_msgs.msg import EventArray


####################################################################################################
# CLASSES
####################################################################################################



####################################################################################################
# DEFINITIONS
####################################################################################################

global e1_l, e1_r
e1_l = e1_r = -1

global pos, vel, eff, acc
pos = vel = eff = acc = []

####################################################################################################
# FUNCTIONS
####################################################################################################

def cbJointState(data):
    global pos, vel, eff
    pos = data.position
    vel = data.velocity
    eff = data.effort
    # print(pos)
    # print(vel)
    # print(eff)


def cbLeftEventArray(data):
    global e1_l
    for e in data.events:
        x = e.x
        y = e.y
        t = e.ts.to_sec()*1000
        p = int(e.polarity)
        # print("%d: (%d,%d) | %d" % (t, x, y, p))


def cbRightEventArray(data):
    global e1_r
    for e in data.events:
        x = e.x
        y = e.y
        t = e.ts.to_sec()*1000
        p = int(e.polarity)
        # print("%d: (%d,%d) | %d" % (t, x, y, p))


####################################################################################################
# MAIN
####################################################################################################


if __name__ == "__main__":

    # Create ROS node (to be able to subscribe/publish to topics)
    rospy.init_node("pathway")
    time.sleep(1)

    # Create publishers, one for each of the 6 motor commands
    head_lr = rospy.Publisher('/robot/RHM0_joint/cmd_pos', Float64, queue_size=1)
    head_ud = rospy.Publisher('/robot/SwingXAxis_joint/cmd_pos', Float64, queue_size=1)
    leye_lr = rospy.Publisher('/robot/ArmRightZAxis_joint/cmd_pos', Float64, queue_size=1)
    reye_lr = rospy.Publisher('/robot/ArmLeftZAxis_joint/cmd_pos', Float64, queue_size=1)
    leye_ud = rospy.Publisher('/robot/CameraMountRightXAxis_joint/cmd_pos', Float64, queue_size=1)
    reye_ud = rospy.Publisher('/robot/CameraMountLeftXAxis_joint/cmd_pos', Float64, queue_size=1)
    ball_x_speed = rospy.Publisher('/x_speed', Float32, queue_size=1)
    ball_y_speed = rospy.Publisher('/y_speed', Float32, queue_size=1)
    ball_z_speed = rospy.Publisher('/z_speed', Float32, queue_size=1)

    # Create subscribers, one for each sensor
    jstates = rospy.Subscriber('/robot/joint_states', JointState, cbJointState, buff_size=1)
    l_dvs = rospy.Subscriber('/head/dvs_left/events', EventArray, cbLeftEventArray, buff_size=1)
    r_dvs = rospy.Subscriber('/head/dvs_right/events', EventArray, cbRightEventArray, buff_size=1)

    # Wait so all the publishers and subscribers are ready ...
    time.sleep(1)

    # Below, two types of head/eye motions are (should be) performed
    open_loop = True
    closed_loop = True

    # 'Mechanical' Limits for Yaw and Pitch of Head and Eyes
    max_h_yaw = math.pi/4
    max_h_pitch = math.pi/8
    max_e_yaw = math.pi/6
    max_e_pitch = math.pi/6

    # OPEN LOOP: without sensory feedback (no subscribers necessary)
    if open_loop:

        t = 2

        # Moving Head RIGHT and LEFT
        head_lr.publish(-max_h_yaw)
        ball_y_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions

        head_lr.publish(max_h_yaw)
        ball_y_speed.publish(-0.5)
        time.sleep(2*t) # Wait for 2*t seconds (to see motion)
        print(pos) # Check current positions

        head_lr.publish(0)
        ball_y_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions
        ball_y_speed.publish(0.0)

        # Moving Head UP and DOWN
        head_ud.publish(-max_h_pitch)
        ball_z_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions

        head_ud.publish(max_h_pitch)
        ball_z_speed.publish(-0.5)
        time.sleep(2*t) # Wait for 2*t seconds (to see motion)
        print(pos) # Check current positions

        head_ud.publish(0)
        ball_z_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions
        ball_z_speed.publish(0.0)

        # Moving Both Eyes RIGHT and LEFT
        leye_lr.publish(-max_e_yaw)
        reye_lr.publish(-max_e_yaw)
        ball_y_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions

        leye_lr.publish(max_e_yaw)
        reye_lr.publish(max_e_yaw)
        ball_y_speed.publish(-0.5)
        time.sleep(2*t) # Wait for 2*t seconds (to see motion)
        print(pos) # Check current positions

        leye_lr.publish(0)
        reye_lr.publish(0)
        ball_y_speed.publish(0.5)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions
        ball_y_speed.publish(0.0)

        # Moving Both Eyes UP and DOWN
        leye_ud.publish(-max_e_pitch)
        reye_ud.publish(-max_e_pitch)
        ball_z_speed.publish(0.1)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions

        leye_ud.publish(max_e_pitch)
        reye_ud.publish(max_e_pitch)
        ball_z_speed.publish(-0.1)
        time.sleep(2*t) # Wait for 2*t seconds (to see motion)
        print(pos) # Check current positions

        leye_ud.publish(0)
        reye_ud.publish(0)
        ball_z_speed.publish(0.1)
        time.sleep(t) # Wait for t seconds (to see motion)
        print(pos) # Check current positions
        ball_z_speed.publish(0.0)


    # CLOSED LOOP: with sensory feedback (subscribers are necessary)
    if closed_loop:

        # USE SENSORY FEEDBACK TO CONTROL MOTION
        print(jstates)
        print(JointState)
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
        pass

    rospy.spin()
