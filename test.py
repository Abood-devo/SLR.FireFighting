from pyPS4Controller.controller import Controller
import os
import sys
sys.path.append('/home/pi/MasterPi/')
import MecanumControl.Car_Drifting_Demo as drif
import MecanumControl.Car_Forward_Demo as fdemo
import MecanumControl.Car_Move_Demo as mdemo
import MecanumControl.Car_Slant_Demo as sdemo
import MecanumControl.Car_Turn_Demo as tdemo
import HiwonderSDK.MotorControlDemo as con
import Camera
cam=Camera.Camera()
drifd=drif.Run()
forw=fdemo.forward()
mo_ve=mdemo.move()
sl_an=sdemo.slant()
tu_rn=tdemo.turn()
co_nt=con.control()
class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    def on_x_press(self):
        drifd.star()
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_x_press")

    #def on_x_release(self):
     #   print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_x_release")

    def on_triangle_press(self):
        forw.for_demo()
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_triangle_press")

    #def on_triangle_release(self):
      #  print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_triangle_release")

    def on_circle_press(self):
        sl_an.slant_demo()
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_circle_press")

    #def on_circle_release(self):
     #   print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_circle_release")

    def on_square_press(self):
        tu_rn.turn_demo()
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_square_press")
   # def on_square_release(self):
        #print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_square_release")

    def on_L1_press(self):
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_L1_press")

    #def on_L1_release(self):
     #   print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_L1_release")

    def on_L2_press(self, value):
        print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_L2_press: {}".format(value))
        
     #   return 'on_L2_press'
   # def on_L2_release(self):
    #    print("rrrrrrrrrrrrrrrrrrrrrrrrr\n-on_L2_release")

    def on_R1_press(self):
        print("on_R1_press")

    #def on_R1_release(self):
     #   print("on_R1_release")

    def on_R2_press(self, value):
        print("on_R2_press: {}".format(value))

   # def on_R2_release(self):
    #    print("on_R2_release")

    def on_up_arrow_press(self):
        print("on_up_arrow_press")
        co_nt.con_demo()

   # def on_up_down_arrow_release(self):
    #    print("on_up_down_arrow_release")

    def on_down_arrow_press(self):
        #cam.camerarun()
        print("on_down_arrow_press")

    def on_left_arrow_press(self):
        #cam.camera_open()
        print("on_left_arrow_press")

    #def on_left_right_arrow_release(self):
     #   print("on_left_right_arrow_release")

    def on_right_arrow_press(self):
        #cam.camera_close()
        print("on_right_arrow_press")

    def on_L3_up(self, value):
        cam.camera_task()
        print("on_L3_up: {}".format(value))

    def on_L3_down(self, value):
        print("on_L3_down: {}".format(value))

    def on_L3_left(self, value):
        print("on_L3_left: {}".format(value))

    def on_L3_right(self, value):
        print("on_L3_right: {}".format(value))

    def on_L3_y_at_rest(self):
        """L3 joystick is at rest after the joystick was moved and let go off"""
        print("on_L3_y_at_rest")

    def on_L3_x_at_rest(self):
        """L3 joystick is at rest after the joystick was moved and let go off"""
        print("on_L3_x_at_rest")

    def on_L3_press(self):
        """L3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_L3_press")

    #def on_L3_release(self):
        """L3 joystick is released after the click. This event is only detected when connecting without ds4drv"""
     #   print("on_L3_release")

    def on_R3_up(self, value):
        print("on_R3_up: {}".format(value))
        

    def on_R3_down(self, value):
        print("on_R3_down: {}".format(value))

    def on_R3_left(self, value):
        print("on_R3_left: {}".format(value))

    def on_R3_right(self, value):
        print("on_R3_right: {}".format(value))

    def on_R3_y_at_rest(self):
        """R3 joystick is at rest after the joystick was moved and let go off"""
        print("on_R3_y_at_rest")

    def on_R3_x_at_rest(self):
        """R3 joystick is at rest after the joystick was moved and let go off"""
        print("on_R3_x_at_rest")

    def on_R3_press(self):
        """R3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_R3_press")

    #def on_R3_release(self):
        """R3 joystick is released after the click. This event is only detected when connecting without ds4drv"""
     #   print("on_R3_release")

    def on_options_press(self):
        print("on_options_press")

   # def on_options_release(self):
    #    print("on_options_release")

    def on_share_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_share_press")

   # def on_share_release(self):
        """this event is only detected when connecting without ds4drv"""
    #    print("on_share_release")

    def on_playstation_button_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_playstation_button_press")

    #def on_playstation_button_release(self):
        """this event is only detected when connecting without ds4drv"""
     #   print("on_playstation_button_release")


class ughzuizgh(MyController):
    def translate(self,value ,minvalue,maxvalue):
        value=(value- minvalue)/maxvalue
        return value
    def on_R3_up(self, value):
        value=translate(value,1,100)
        return value
    
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
