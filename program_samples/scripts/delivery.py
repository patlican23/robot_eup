#!/usr/bin/env python
import argparse
import rospy
import pr2_eup
from pr2_eup.robot import Robot

def do_delivery(robot):
    
    #location_names = [name for name, location in location_db.get_all_locations()]
    #location = robot.interface.ask_choice('Please choose a location.', location_names)
    #rospy.loginfo('Delivering item to {}'.format(location))
    
    #pose_stamped = location_db.get_location(location)

    choice = robot.interface.ask_choice('Press Start when you are ready:', ['Start'])

    Robot.start(robot.interface.say_message('Moving backward..', timeout=2))
    Robot.do(robot.navigation.move_backward, {'duration':'3'})
    Robot.do(robot.interface.say_message('Done Moved backward..', timeout=1))

    choice = Robot.do(robot.interface.ask_choice('Press Start when you are ready:', ['continue']))

    navigation_monitor = Robot.start(robot.navigation.move_forward, {'duration':'2'})
    Robot.wait(navigation_monitor)
    Robot.do(robot.navigation.turn_left, {'duration':'2'})
    robot.interface.say_message('Moved forward..', timeout=1)
    #robot.navigation.move_forward(2)

    #robot.navigation.turn_right(2)
    #robot.interface.say_message('Turned right..', timeout=1)

    #robot.navigation.turn_left(2)
    #robot.interface.say_message('Turned left..', timeout=1)

    #choice = robot.interface.ask_choice('Which direction should the robot move?.', ['forward', 'backward'])

if __name__ == '__main__':
    rospy.init_node('delivery')
    robot = pr2_eup.RobotFactory().build()
    #parser = argparse.ArgumentParser()
    #parser.add_argument('filename',
    #                    metavar='FILE',
    #                    type=str,
    #                    help='Python shelve DB containing locations.')
    #args = parser.parse_args(args=rospy.myargv()[1:])
    #location_db = robot.location_db(args.filename)

    while not rospy.is_shutdown():
        do_delivery(robot)