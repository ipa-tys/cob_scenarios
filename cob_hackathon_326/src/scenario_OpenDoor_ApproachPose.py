#!/usr/bin/python

import roslib
roslib.load_manifest('cob_hackathon_326')
import rospy
import smach
import smach_ros
from ApproachPose import *
from WaitForOpenElevatorDoors import *
from simple_script_server import *  # import script
sss = simple_script_server()

class SM1(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self,outcomes=['ended','failed'])
        with self:
            #  [-0.378, -6.839, 1.476]
            smach.StateMachine.add('APPROACH_POSE',ApproachPose([-0.2,-3.9,1.4]),transitions={'reached':'WAITFOROPENDOOR', 'not_reached':'ended', 'failed':'failed'})
            smach.StateMachine.add('WAITFOROPENDOOR',WaitForOpenElevatorDoors(rospy.Duration(15)),transitions={'door_open':'APPROACH_ENDPOSE', 'door_closed':'ended', 'failed':'failed'})
            smach.StateMachine.add('APPROACH_ENDPOSE',ApproachPose(),transitions={'reached':'ended', 'not_reached':'ended', 'failed':'failed'})

def main():
    rospy.init_node('AUTOMATICA2012')
    #sm = smach.StateMachine(outcomes=['ended'])
    #with sm:
    #    smach.StateMachine.add('FOO', HierSM1(),
    #                          transitions={'succeeded1':'ended'})
    
    sm = SM1()

    sis = smach_ros.IntrospectionServer('AUTOMATICA2012', sm, 'AUTOMATICA2012')
    sis.start()

    outcome = sm.execute()

    rospy.spin()
    sis.stop()
    
if __name__=='__main__':
    main()
