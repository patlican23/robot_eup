#!/usr/bin/env python
import rospy
import pr2_eup
from pr2_eup.msg import RobotType

#############################################

def main_loop(robot):
    robot.display_message(message='Hello, my name is Chester.', duration=3)
    
    choice = robot.ask_choice(message='What should I do?', choices=['Dance', 'Sing'])
    if choice == 'Dance':
        robot.turn_right(duration=1)
        robot.turn_left(duration=1)
        robot.turn_right(duration=1)
        robot.turn_left(duration=1)
    else:
        robot.play_sound(sound_name='sound1')
        robot.play_sound(sound_name='sound2')
        robot.play_sound(sound_name='sound3')

    robot.say(text='Now, lets speak. What should I do?')
    command = robot.wait_for_speech()
        
    if command == 'one':
        robot.move(x=0.5, y=0.0, theta=0, duration=1)
    elif command == 'two':
        robot.move(x=-0.5, y=0.0, theta=0, duration=1)
    else:
        robot.say(text='I could not hear you.')

    robot.display_message(message='Going to drive now', duration=3)
    robot.go_to(location_name='B')

#############################################

if __name__ == '__main__':
    rospy.init_node('pr2_eup_example1')
    robot = pr2_eup.RobotFactory().build(RobotType.TURTLEBOT)
    robot.start_robot()
    while not rospy.is_shutdown():
        main_loop(robot)
