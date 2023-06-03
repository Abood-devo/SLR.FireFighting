#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/MasterPi/')
import time
import signal
import HiwonderSDK.mecanum as mecanum
from HiwonderSDK.Board import setBuzzer, setPWMServoPulse, setPWMServoAngle
from HiwonderSDK.Misc import map 
from pyPS4Controller.controller import Controller

chassis = mecanum.MecanumChassis()

being_controlled = 'robot'

def Stop():
    print("stopping")
    chassis.set_velocity(0,0,0)  # turn off all motors

class MyControllerRobot(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    # ------------------------ Robot Movement ------------------------
    def on_R2_press(self, value):
        speed = map(value, -32431, 32767, 0, 100)
        chassis.set_velocity(speed,90,0)

    def on_L2_press(self, value):
        speed = map(value, -32431, 32767, 0, -100)
        chassis.set_velocity(speed,90,0)
    
    def on_R3_left(self, value):
        speed = map(-1*value, 0, 32767, 0, 100)
        chassis.set_velocity(speed,180,0)

    def on_R3_right(self, value):
        speed = map(value, 0, 32767, 0, 100)
        chassis.set_velocity(speed,0,0)

    def on_L3_right(self, value):
        rotational_speed = map(-1*value, 0, 32767, 0, -2)
        chassis.set_velocity(0,90,rotational_speed)    # rotate clockwise

    def on_L3_left(self, value):
        rotational_speed = map(value, 0, 32767, 0, 2)
        chassis.set_velocity(0,90,rotational_speed)# rotate counterclockwise
    
    def on_x_press(self):
        chassis.set_velocity(40,50,0)# rotate counterclockwise

    # ------------------------ Robot Movement ------------------------
    # Movement stopping functions
    def on_R2_release(self):
        Stop()
    def on_R3_x_at_rest(self):
        Stop()
    def on_R3_y_at_rest(self):
        Stop()
    def on_L3_x_at_rest(self):
        Stop()
    def on_L3_y_at_rest(self):
        Stop()
    def on_L2_release(self):
        Stop()
    def on_x_release(self):
        Stop()
    def on_options_press(self):
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        
        print("exiting")
        exit()
    # switch to arm control
    def on_playstation_button_press(self):
        global being_controlled
        being_controlled = 'arm'
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        self.stop = True
        print(being_controlled)

class MyControllerArm(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    # ------------------------ Arm Movement ------------------------
    def on_R2_press(self, value):
        angle = int(map(value, -32431, 32767, 500, 2500))
        setPWMServoPulse(1, angle,1000)

    def on_L2_press(self, value):
        angle = int(map(value, -32431, 32767, 2000, 1500))
        setPWMServoPulse(1, angle,1000)
    
    def on_R3_left(self, value):
        angle = int(map(-1*value,0, 32767, 1500, 2500))
        setPWMServoPulse(6, angle,1000)

    def on_R3_right(self, value):
        angle = int(map(value, 0, 32767, 1500, 500))
        setPWMServoPulse(6, angle,1000)

    def on_R3_up(self, value):
        angle = int(map(-1*value,0, 32767, 1500, 2500))
        setPWMServoPulse(5, angle,800)

    def on_R3_down(self, value):
        angle = int(map(value, 0, 32767, 1500, 500))
        setPWMServoPulse(5, angle,800)

    def on_L3_up(self, value):
        angle = int(map(-1*value,0, 32767, 1500, 2500))
        setPWMServoPulse(4, angle,800)

    def on_L3_down(self, value):
        angle = int(map(value, 0, 32767, 1500, 500))
        setPWMServoPulse(4, angle,800)

    def on_L3_left(self, value):
        angle = int(map(-1*value,0, 32767, 1500, 2500))
        setPWMServoPulse(3, angle,1000)

    def on_L3_right(self, value):
        angle = int(map(value, 0, 32767, 1500, 500))
        setPWMServoPulse(3, angle,1000)

    def on_R1_press(self):
        setPWMServoPulse(1, 1500, 1000)
        setPWMServoPulse(3, 500, 1000)
        setPWMServoPulse(4, 2130, 1000)
        setPWMServoPulse(5, 2382, 1000)
        setPWMServoPulse(6, 1500,1000)

    def on_L1_press(self):
        setPWMServoPulse(3, 2500, 1000)
        setPWMServoPulse(4, 829, 1000)
        setPWMServoPulse(5, 1747, 1000)
        setPWMServoPulse(6, 1500,1000)
        time.sleep(1)
        setPWMServoPulse(1, 2500, 500)
        

    def on_x_press(self):
        setPWMServoAngle(1, 0)
        setPWMServoAngle(3, 0)
        setPWMServoAngle(4, 0)
        setPWMServoAngle(5, 0)
        setPWMServoAngle(6, 0)
    # ------------------------ Arm Movement ------------------------
    # Movement stopping functions
    # def on_R2_release(self):
    #     Stop()
    # def on_R3_x_at_rest(self):
    #     Stop()
    # def on_R3_y_at_rest(self):
    #     Stop()
    # def on_L3_x_at_rest(self):
    #     Stop()
    # def on_L3_y_at_rest(self):
    #     Stop()
    # def on_L2_release(self):
    #     Stop()
    def on_options_press(self):
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        time.sleep(0.1) # delay
        print("exiting")
        exit()
    # switch to arm control
    def on_playstation_button_press(self):
        global being_controlled
        being_controlled = 'robot'
        setBuzzer(1) # open
        time.sleep(0.2) # delay
        setBuzzer(0) #close 
        self.stop = True
        print(being_controlled)

       
if __name__ == '__main__':
    while True:
        controller_robot = MyControllerRobot(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller_robot.listen(timeout=60)

        controller_arm = MyControllerArm(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller_arm.listen(timeout=60)

    print('turned off')