import RPi.GPIO  as  GPIO
import  time
GPIO.setwarnings(False)

LedPin = 18         # pin11 
LedPin2 = 15         # pin11 
def setup():      
    GPIO.setmode(GPIO.BOARD)       # Set the board mode  to numbers pins by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
    GPIO.setup(LedPin2, GPIO.OUT)   # Set pin mode as output
    GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led
    # GPIO.setup(13,GPIO.OUT) 

def loop():     
  while True:            
         GPIO.output(LedPin, GPIO.LOW)   # led on
         time.sleep(3.0)                                  # wait 1 sec    
         GPIO.output(LedPin2, GPIO.LOW)   # led on
         time.sleep(5.0)                                  # wait 1 sec    
         GPIO.output(LedPin, GPIO.HIGH)  # led off
         time.sleep(5.0)     
         GPIO.output(LedPin2, GPIO.HIGH)   # led on
                                      # wait 1 sec
def destroy():
        GPIO.output(LedPin, GPIO.HIGH)     # led off
        GPIO.output(LedPin2, GPIO.HIGH)     # led off
        GPIO.cleanup()                                    # Release resource

if __name__ == '__main__':                  # Program start from here
        print("start")
        setup()
        try:
                loop()
        except KeyboardInterrupt:            # When 'Ctrl+C' is pressed, the destroy() will be  executed.
               destroy()