from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction
import signal
import time
from threading import Lock
from event_monitor import EventMonitor

class Navigation(object):
    def __init__(self, base_frame, world_frame, tf_listener):

        self._move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self._base_controller_publisher = rospy.Publisher('/base_controller/command', Twist, queue_size=10)

        self._base_frame = base_frame
        self._world_frame = world_frame
        self._tf_listener = tf_listener
        self._base_lock = Lock()

    def move_forward(self, duration):
        return self.move(0.75, 0, 0, duration)

    def move_backward(self, duration):
        return self.move(-0.75, 0, 0, duration)

    def turn_left(self, duration):
        return self.move(0, 0, 0.75, duration)

    def turn_right(self, duration):
        return self.move(0, 0, -0.75, duration)

    def _move_forever(self, x, y, theta):
        twist_msg = Twist()
        twist_msg.linear = Vector3(x, y, 0.0)
        twist_msg.angular = Vector3(0.0, 0.0, theta)
        while True:
            self._base_controller_publisher.publish(twist_msg)
            time.sleep(0.05)

    def _move_once(self, x, y, theta):
        twist_msg = Twist()
        twist_msg.linear = Vector3(x, y, 0.0)
        twist_msg.angular = Vector3(0.0, 0.0, theta)
        self._base_controller_publisher.publish(twist_msg)

    def move(self, x, y, theta, duration):

        if self._base_lock.locked():
            rospy.logwarn('Received base movement request while busy, will have to wait.')
        self._base_lock.acquire()
        start_time = time.time()
        current_time = time.time()
        while (current_time-start_time < float(duration)):
            self._move_once(x, y, theta)
            time.sleep(0.01)
            current_time = time.time()
        self._move_once(0, 0, 0)
        self._base_lock.release()
        return None

    def go_to(self, pose_stamped):
        """Goes to a location in the world.

        Args:
          pose_stamped: geometry_msgs/PoseStamped. The location to go to.
        """
        self._move_base_client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose = pose_stamped
        self._move_base_client.send_goal(goal)
        self._move_base_client.wait_for_result()

    def get_current_location(self):
        """Returns the location of the robot in the world frame.

        Returns: geometry_msgs/PoseStamped. The pose of the robot in the world
          frame, or None if it couldn't figure out its location.
        """
        try:
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = self._base_frame
            pose_stamped.header.stamp = rospy.Time(0)
            pose_stamped.pose.position.x = 0
            pose_stamped.pose.position.y = 0
            pose_stamped.pose.position.z = 0
            pose_stamped.pose.orientation.w = 1
            pose_stamped.pose.orientation.x = 0
            pose_stamped.pose.orientation.y = 0
            pose_stamped.pose.orientation.z = 0
            current_location = self._tf_listener.transformPose(
                self._world_frame, pose_stamped)
            return current_location
        except Exception as e:
            rospy.logerr(
                'Failed to get current pose in world frame {}.'.format(
                    self._world_frame))
            rospy.logerr(e)
            return None