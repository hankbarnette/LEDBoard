#The Real Deal

import RPi.GPIO as GPIO
import time

#PIN LIST (GPIO - PHYSICAL PIN)
GPIO1 = 12

#Define LEDs
LED_GREEN = GPIO1


#GPIO Initiallization
#reference the pins on the board
GPIO.setmode(GPIO.BOARD)

#Configure LED pin mode       
GPIO.setup(LED_GREEN,GPIO.OUT)



def greenOn():
    print("Green On")
    #Turn on Green LED
    GPIO.output(LED_GREEN,GPIO.HIGH)
    return

def greenOff():
    print("Green Off")
    GPIO.output(LED_GREEN,GPIO.LOW)
    return

def destroy():
    print("QUITTING")
    greenOff()
    GPIO.cleanup()
    return


def main():

    try:
        greenOn()
        
        
    except KeyboardInterrupt: 
        #release our resources
        print("pressed")
        destroy()


#Start this thing
main()
