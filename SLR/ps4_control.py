#!/usr/bin/python3
# coding=utf8
import HiwonderSDK.mecanum as mecanum
import sys
import time
from HiwonderSDK import Board as brd
from HiwonderSDK.Misc import map
from ArmIK import ArmMoveIK as arm
import RPi.GPIO  as  GPIO

from pyPS4Controller.controller import Controller
sys.path.append('/home/pi/RAS.FireFighting/SLR/')

chassis = mecanum.MecanumChassis()
AK = arm.ArmIK()

joint_angels = AK.getAllPWMAngels()

servo = {'servo1': 1, 'servo3': 3, 'servo4': 4, 'servo5': 5, 'servo6': 6}

increments = [None, 10, None, 1, 14, 2, 10]

joint_limits_p = [None, (500, 2500), None,
                  (0, 180), (500, 2500), (0, 180), (500, 2500)]
use_time = 100
being_controlled_servo_id = 5
to_control_servo_ids = [3, 4, 5]

global release_state
release_state = False

global gripper_state
gripper_state = False

pumpPin = 15 
valvePin = 18 
GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(valvePin, GPIO.OUT)
GPIO.output(pumpPin, GPIO.HIGH)
GPIO.output(valvePin, GPIO.HIGH)

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
    # brd.setPWMServoPulse(1, 1500, 1000)
    # brd.setPWMServoPulse(3, 2400, 1000)
    # brd.setPWMServoPulse(4, 2500, 1000)
    # brd.setPWMServoPulse(5, 2500, 1000)
    # brd.setPWMServoPulse(6, 1500, 1000)

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
    # arm_init()


class MyControllerRobot(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    # ------------------------ START Robot Movement ------------------------

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
    def on_circle_press(self):
        global gripper_state
        if gripper_state:
            brd.setPWMServoPulse(1, 1500, 500) 
            gripper_state = not gripper_state
        else:
            brd.setPWMServoPulse(1, 2000, 500)
            gripper_state = not gripper_state

    def on_R2_press(self, value):
        servo_id = servo['servo3']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)-increments[servo_id])


    def on_L2_press(self, value):
        servo_id = servo['servo3']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)+increments[servo_id])

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
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)+increments[servo_id])

    def on_up_arrow_press(self):
        servo_id = servo['servo4']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)-increments[servo_id])

    def on_L3_down(self, value):
        servo_id = servo['servo5']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)-increments[servo_id])

    def on_L3_up(self, value):
        servo_id = servo['servo5']
        brd.setPWMServoAngle(servo_id, brd.getPWMServoAngle(servo_id)+increments[servo_id])
        # ------------------------ START arm macros ------------------------

    def on_R1_press(self):
        """this method is used to reaset the arm to the best balance position"""
        brd.setPWMServoPulse(1, 1500, 1610)
        brd.setPWMServoPulse(3, 2140 , 1610)
        brd.setPWMServoPulse(4, 500, 1610)
        brd.setPWMServoPulse(6, 1560, 1610)
        brd.setPWMServoPulse(5, 2288, 1610)

    def on_L1_press(self):
        """this method is used to release the ball into the container"""
        global release_state
        if release_state: 
            brd.setPWMServoPulse(3, 2500, 1200)
            brd.setPWMServoPulse(4, 500, 1200)
            brd.setPWMServoPulse(6, 1800, 1200)
            brd.setPWMServoPulse(5, 950, 1200)
            time.sleep(1.5)
            brd.setPWMServoPulse(1, 2000, 500)
            release_state = not release_state
        else:
            brd.setPWMServoPulse(3, 500, 1200)
            brd.setPWMServoPulse(4, 2500, 1200)
            brd.setPWMServoPulse(6, 1500, 1200)
            brd.setPWMServoPulse(5, 1960, 1200)
            time.sleep(1.5)
            brd.setPWMServoPulse(1, 2000, 500)
            release_state = not release_state
    
    def on_share_press(self):
        """
        sets the arm in the pos of tunnel ball pik
        """
        brd.setPWMServoPulse(3, 1500, 1200)
        brd.setPWMServoPulse(4, 590, 1200)
        brd.setPWMServoPulse(6, 1500, 1200)
        brd.setPWMServoPulse(5, 1500, 1200)
        time.sleep(1.5)
        brd.setPWMServoPulse(1, 2170, 500)
        # ------------------------ END arm macros ------------------------
    # ------------------------ END ARM Movement ------------------------

    # ------------------------ START functionalities ------------------------
    def on_options_press(self):
        """
        stoping control
        """
        exit_exec()

    def on_x_press(self):
         GPIO.output(pumpPin, GPIO.LOW)
    
    def on_x_release(self):
         GPIO.output(pumpPin, GPIO.HIGH)
    
    def on_triangle_press(self):
         GPIO.output(valvePin, GPIO.LOW)
    
    def on_triangle_release(self):
         GPIO.output(valvePin, GPIO.HIGH)

    def on_playstation_button_press(self):
        chassis.set_velocity(60, 180, 0)
        time.sleep(0.6)
        chassis.stopMovement()
        
        chassis.set_velocity(60, 90, 0)
        time.sleep(1.7)
        chassis.stopMovement()

        chassis.set_velocity(60, 180, 0)
        time.sleep(0.5)
        chassis.stopMovement()
        
        chassis.set_velocity(0, 90, -0.3)
        time.sleep(0.5)
        chassis.stopMovement()

        chassis.set_velocity(60, 90, 0)
        time.sleep(0.6)
        chassis.stopMovement()

        brd.setPWMServoPulse(3, 2335, 1200)
        brd.setPWMServoPulse(4, 1112, 1200)
        brd.setPWMServoPulse(6, 1347, 1200)
        brd.setPWMServoPulse(5, 2265, 1200)
        time.sleep(1.5)
        brd.setPWMServoPulse(1, 1500, 500)

        # set arm to pos
        # brd.setPWMServoPulse(3, 2453, 1200)
        # brd.setPWMServoPulse(4, 1276, 1200)
        # brd.setPWMServoPulse(6, 2500, 1200)
        # brd.setPWMServoPulse(5, 2382, 1200)
        # time.sleep(1.5)
        # brd.setPWMServoPulse(1, 1500, 500)
        
        brd.Buzz(timer=0.5)
        brd.Buzz(timer=0.1)
        brd.Buzz(timer=0.1)
        # chassis.set_velocity(60, 90, 0)
        # time.sleep(4.4)
        # chassis.stopMovement()

    # ------------------------ END functionalities ------------------------


if __name__ == '__main__':
    brd.Buzz(timer=0.2)
    brd.turnOnLed(0, (0, 0, 255))
    brd.turnOnLed(1, (0, 0, 255))
    controller_robot = MyControllerRobot(interface="/dev/input/js0",
                                         connecting_using_ds4drv=False)
    while True:
        try:
            controller_robot.listen(timeout=10000, on_connect=on_connect)
        except KeyboardInterrupt:
            break
        except:
            continue
