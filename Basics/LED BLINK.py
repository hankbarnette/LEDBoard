#BLINKS LED ON AND OFF

import RPi.GPIO as GPIO
import time

#LEDPIN LIST
PIN7 = 7
PIN6 = 22
PIN5 = 18
PIN4 = 16
PIN2 = 13
PIN3 = 15
#PINS=[PIN7,PIN6,PIN5,PIN4]
PINS=[PIN7,PIN6,PIN5,PIN4,PIN3,PIN2]
#vanity names
LedPins=[PIN7,PIN6,PIN5,PIN4]
ButtonPin = PIN3
GreenLed  = PIN2




#GPIO Initiallization
#reference the pins on the board
GPIO.setmode(GPIO.BOARD)


def setupPins(pinlist):
    #SETUP LEDS
    for pin in pinlist:
        print("Configuring PIN: " + str(pin))
        #setup the pin so it is an output PIN        
        GPIO.setup(pin,GPIO.OUT)
    #SETUP BUTTON
    GPIO.setup(ButtonPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #SETUP GREENLED
    GPIO.setup(GreenLed,GPIO.OUT)
    GPIO.output(GreenLed,GPIO.LOW)
    
    return

def ledLoop(pinlist,speed):
    for pin in pinlist:
        ledOn(pin)
        pause(speed)
        ledOff(pin)
        pause(speed) 
    return

def ledOn(PIN):
    print(str(PIN) + " ON")
    GPIO.output(PIN,GPIO.LOW)    
    return

def ledOff(PIN):
    print(str(PIN) + " OFF")
    GPIO.output(PIN,GPIO.HIGH)    
    return

def shutdownLeds(pinlist):
    for pin in pinlist:
        ledOff(pin)    
    return

def pause(miliseconds):
    #print("Pausing for " + str(miliseconds) + " seconds")
    time.sleep(miliseconds)
    return


def cycleGreen():
    #run green light
    powerlevel = GPIO.PWM(GreenLed, 1000) #set frequency to 1khz
    powerlevel.start(0) #starting value of 0 duty cycles
    #turn on green led
    for dutycycle in range(0,101,15):
        powerlevel.ChangeDutyCycle(dutycycle)
        time.sleep(0.05)
    #brief pause
    time.sleep(.5)
    #turn off green led
    for dutycycle in range(100,-1,-25):
        powerlevel.ChangeDutyCycle(dutycycle)
        time.sleep(0.05)
    #cleanup
    powerlevel.stop()

def watchButton():        
        #run the loop forever        
        while True:           
            
            if GPIO.input(ButtonPin) == GPIO.LOW:
                print("Button pushed")
                #run the led loop
                ledLoop(LedPins,.01)
            else:
                #not pushed
                cycleGreen()
                        
            

def destroy():
    print("QUITTING")
    shutdownLeds(LedPins)
    GPIO.cleanup()



#----------------------------------------------------


#configure the PINS
setupPins(PINS)


try:
    watchButton()
    
except KeyboardInterrupt:     
    #release our resources
    destroy()

    
    
