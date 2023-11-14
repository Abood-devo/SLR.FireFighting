#!/usr/bin/python3
# coding=utf8
import HiwonderSDK.mecanum as mecanum
import sys
import time
from HiwonderSDK import Board as brd
from HiwonderSDK.Misc import map
from ArmIK import ArmMoveIK as arm
# from VisualPatrol import *
from pyPS4Controller.controller import Controller
sys.path.append('/home/pi/RAS.FireFighting/MasterPi/')

chassis = mecanum.MecanumChassis()
AK = arm.ArmIK()

joint_angels = AK.getAllPWMAngels()

servo = {'servo1': 1, 'servo3': 3, 'servo4': 4, 'servo5': 5, 'servo6': 6}

increments = [None, 10, None, 10, 14, 2, 10]

joint_limits_p = [None, (500, 2500), None,
                  (0, 180), (500, 2500), (0, 180), (500, 2500)]
use_time = 100
being_controlled_servo_id = 5
to_control_servo_ids = [3, 4, 5]


def arm_init():
    brd.setPWMServoPulse(1, 1500, 1000)
    brd.setPWMServoPulse(3, 500, 1000)
    brd.setPWMServoPulse(4, 2500, 1000)
    brd.setPWMServoPulse(5, 1040, 1000)
    brd.setPWMServoPulse(6, 1500, 1000)


def exit_exec():
    """
    stop the execution of the script
    """
    # resting arm
    brd.setPWMServoPulse(1, 1500, 1000)
    brd.setPWMServoPulse(3, 2400, 1000)
    brd.setPWMServoPulse(4, 2500, 1000)
    brd.setPWMServoPulse(5, 2500, 1000)
    brd.setPWMServoPulse(6, 1500, 1000)

    brd.Buzz(timer=0.2)
    time.sleep(0.1)

    brd.Buzz(timer=0.2)
    time.sleep(0.1)

    brd.Buzz(timer=0.2)
    time.sleep(0.1)
    print("exiting")
    brd.turnOnLed(0, (255, 0, 0))
    brd.turnOnLed(1, (255, 0, 0))
    exit()


def on_connect():
    """
    things to execute when the ps4 controller connects via bluetooth
    """
    brd.turnOnLed(0, (0, 255, 0))
    brd.turnOnLed(1, (0, 255, 0))

    brd.Buzz(timer=0.2)
    time.sleep(0.1)
    brd.Buzz(timer=0.2)
    arm_init()


class MyControllerRobot(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    # ------------------------ START Robot Movement ------------------------
    def on_circle_press(self):
    	brd.setBuzzer(1)
    def on_circle_realese(self):
   	 brd.setBuzzer(0)
    def on_R3_up(self, value):
        """
        moving forward
        """
        speed = map(abs(value), 0, 32767, 0, 100)
        chassis.set_velocity(speed, 90, 0)

    def on_R3_down(self, value):
        """
        moving forward
        """
        speed = map(value, 0, 32767, 0, -100)
        chassis.set_velocity(speed, 90, 0)

    def on_R3_left(self, value):
        """
        turning left
        """
        rotational_speed = map(value, 0, 32767, 0, 2)
        chassis.set_velocity(0, 90, rotational_speed)

    def on_R3_right(self, value):
        """
        turning right
        """
        rotational_speed = map(-1*value, 0, 32767, 0, -2)
        chassis.set_velocity(0, 90, rotational_speed)

    def on_right_arrow_press(self):
        """
        sliding right
        """
        chassis.set_velocity(60, 0, 0)

    def on_left_arrow_press(self):
        """
        sliding left
        """
        chassis.set_velocity(60, 180, 0)

    # Movement stopping functions
    def on_R3_x_at_rest(self):
        chassis.stopMovement()

    def on_R3_y_at_rest(self):
        chassis.stopMovement()

    def on_left_right_arrow_release(self):
        chassis.stopMovement()
    # ------------------------ END Robot Movement ------------------------
    # ------------------------ START Arm Movement ------------------------

    def on_R2_press(self, value):
        servo_id = servo['servo1']
        if (value >= 0):
            grepping_deg = int(map(value, 0, 32767, 1550, 2500))
            brd.setPWMServoPulse(servo_id, grepping_deg, 500)

    def on_L2_press(self, value):
        servo_id = servo['servo3']
        if (value >= 0):
            grepping_deg = int(map(value, 0, 32767, 500, 2500))
            brd.setPWMServoPulse(servo_id, grepping_deg, 500)

    def on_L3_left(self, value):
        """
        contolling servo 6 (base) positive
        """
        servo_id = servo['servo6']
        AK.jointMove(servo_id=servo_id,
                     positive=True,
                     increment=increments[servo_id],
                     limits=joint_limits_p[servo_id],
                     use_time=use_time)

    def on_L3_right(self, value):
        """
        contolling servo 6 (base) nigative
        """
        servo_id = servo['servo6']
        AK.jointMove(servo_id=servo_id,
                     positive=False,
                     increment=increments[servo_id],
                     limits=joint_limits_p[servo_id],
                     use_time=use_time)

    def on_down_arrow_press(self):
        servo_id = servo['servo4']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)-increments[servo_id])

    def on_up_arrow_press(self):
        servo_id = servo['servo4']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)+increments[servo_id])

    def on_L3_down(self, value):
        servo_id = servo['servo5']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)-increments[servo_id])

    def on_L3_up(self, value):
        servo_id = servo['servo5']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)+increments[servo_id])
        # ------------------------ START arm macros ------------------------

    def on_R1_press(self):
        brd.setPWMServoPulse(1, 1500, 1000)
        brd.setPWMServoPulse(3, 500, 1000)
        brd.setPWMServoPulse(4, 2130, 1000)
        brd.setPWMServoPulse(5, 2382, 1000)
        brd.setPWMServoPulse(6, 1500, 1000)

    def on_L1_press(self):
        brd.setPWMServoPulse(3, 2500, 1000)
        brd.setPWMServoPulse(4, 829, 1000)
        brd.setPWMServoPulse(5, 1747, 1000)
        brd.setPWMServoPulse(6, 1500, 1000)
        time.sleep(1)
        brd.setPWMServoPulse(1, 2500, 500)
        # ------------------------ END arm macros ------------------------
    # ------------------------ END ARM Movement ------------------------

    # ------------------------ START functionalities ------------------------
    def on_options_press(self):
        """
        stoping control
        """
        exit_exec()

    def on_share_press(self):
        """
        automation starter
        """
    #    ssss()
    # ------------------------ END functionalities ------------------------


if __name__ == '__main__':
    brd.Buzz(timer=0.2)
    brd.turnOnLed(0, (0, 0, 255))
    brd.turnOnLed(1, (0, 0, 255))
    controller_robot = MyControllerRobot(interface="/dev/input/js0",
                                         connecting_using_ds4drv=False)
    controller_robot.listen(timeout=1000, on_connect=on_connect)
