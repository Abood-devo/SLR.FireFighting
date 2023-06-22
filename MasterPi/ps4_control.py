#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/MasterPi/')
import time
import HiwonderSDK.mecanum as mecanum
from HiwonderSDK import Board as brd
from HiwonderSDK.Misc import map 
from ArmIK import ArmMoveIK as arm
# from VisualPatrol import *
from pyPS4Controller.controller import Controller


chassis = mecanum.MecanumChassis()
AK = arm.ArmIK()

def arm_init():
    brd.setPWMServoPulse(1, 1500, 1000)
    brd.setPWMServoPulse(3, 1500, 1000)
    brd.setPWMServoPulse(4, 1500, 1000)
    brd.setPWMServoPulse(5, 1500, 1000)
    brd.setPWMServoPulse(6, 1500, 1000)

def exit_exec():
        """
        stop the execution of the script
        """
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
        self.x_value = 0
        self.y_value = 0
        self.z_value = 0
    # ------------------------ START Robot Movement ------------------------
    def on_R3_up(self, value):
        """
        moving forward
        """
        speed = map(abs(value), 0, 32767, 0, 100)
        print(speed)
        chassis.set_velocity(speed,90,0)

    def on_R3_down(self, value):
        """
        moving forward
        """
        speed = map(value, 0, 32767, 0, -100)
        chassis.set_velocity(speed,90,0)
    
    def on_R3_left(self, value):
        """
        turning left
        """
        rotational_speed = map(value, 0, 32767, 0, 2)
        chassis.set_velocity(0,90,rotational_speed)

    def on_R3_right(self, value):
        """
        turning right
        """
        rotational_speed = map(-1*value, 0, 32767, 0, -2)
        chassis.set_velocity(0,90,rotational_speed)

    def on_right_arrow_press(self):
        """
        sliding right
        """
        chassis.set_velocity(60,0,0)

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
        if (value >= 0):
            grepping_deg = int(map(value, 0, 32767, 1400, 2500))
            brd.setPWMServoPulse(1, grepping_deg,500)

    def on_L3_left(self, value):
        motor_pos = brd.getPWMServoPulse(6)
        print(motor_pos-10)
        brd.setPWMServoPulse(6, motor_pos-10, 80)

    def on_L3_right(self, value):
        motor_pos = brd.getPWMServoPulse(6)
        print(motor_pos+10)
        brd.setPWMServoPulse(6, motor_pos+8, 100)

    def on_L3_down(self, value):
        motor_pos = brd.getPWMServoPulse(5)
        print(motor_pos+10)
        brd.setPWMServoPulse(5, motor_pos+10, 80)
    
    def on_L3_up(self, value):
        motor_pos = brd.getPWMServoPulse(5)
        print(motor_pos-10)
        brd.setPWMServoPulse(5, motor_pos-8, 100)  
    
    def on_R1_press(self):
        brd.setPWMServoPulse(1, 1500, 1000)
        brd.setPWMServoPulse(3, 500, 1000)
        brd.setPWMServoPulse(4, 2130, 1000)
        brd.setPWMServoPulse(5, 2382, 1000)
        brd.setPWMServoPulse(6, 1500,1000)

    def on_L1_press(self):
        brd.setPWMServoPulse(3, 2500, 1000)
        brd.setPWMServoPulse(4, 829, 1000)
        brd.setPWMServoPulse(5, 1747, 1000)
        brd.setPWMServoPulse(6, 1500,1000)
        time.sleep(1)
        brd.setPWMServoPulse(1, 2500, 500)

    # ------------------------ END ARM Movement ------------------------
    
    def on_options_press(self):
        exit_exec()

    # switch to arm control
    def on_playstation_button_press(self):
        brd.Buzz(timer=0.2)
        self.stop = True
    
    def on_share_press(self):
       ssss()

if __name__ == '__main__':
    brd.Buzz(timer=0.2)
    brd.turnOnLed(0, (0, 0, 255))
    brd.turnOnLed(1, (0, 0, 255))
    
    controller_robot = MyControllerRobot(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller_robot.listen(timeout=1000, on_connect=on_connect)
