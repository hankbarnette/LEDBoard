#Speech Reconition for LED Marquee

#The Real Deal

import RPi.GPIO as GPIO
import time
import speech_recognition as sr

#PIN LIST (GPIO - PHYSICAL PIN)
GPIO1 = 12
GPIO0 = 11
GPIO2 = 13
GPIO3 = 15

#Recording Settings
CHUNK = 8192
CHANNELS = 1
RATE = 44100
DEVICE_CHANNEL = 2


#Define LEDs
LED_GREEN = GPIO1
LED_YELLOW = GPIO2
LED_RED = GPIO3
BUTTON_ONE = GPIO0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_GREEN,GPIO.OUT)
    GPIO.output(LED_GREEN,GPIO.LOW)
    GPIO.setup(LED_YELLOW,GPIO.OUT)
    GPIO.output(LED_YELLOW,GPIO.LOW)
    GPIO.setup(LED_RED,GPIO.OUT)
    GPIO.output(LED_RED,GPIO.LOW)
    GPIO.setup(BUTTON_ONE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def greenOn():
    #print("Green On")    
    GPIO.output(LED_GREEN,GPIO.HIGH)    

def greenOff():
    #print("Green Off")
    GPIO.output(LED_GREEN,GPIO.LOW)

def yellowOn():
    #print("Green On")    
    GPIO.output(LED_YELLOW,GPIO.HIGH)    

def yellowOff():
    #print("Green Off")
    GPIO.output(LED_YELLOW,GPIO.LOW)

def redOn():
    #print("Green On")    
    GPIO.output(LED_RED,GPIO.HIGH)    

def redOff():
    #print("Green Off")
    GPIO.output(LED_RED,GPIO.LOW)
        
def destroy():
    print("QUITTING")
    greenOff()
    yellowOff()
    redOff()
    GPIO.cleanup()

def detectSpeech():    
    r = sr.Recognizer()
    r.energy_threshold = 3000
    #Turn off Greed LED
    greenOff()
    
    with sr.Microphone(device_index=DEVICE_CHANNEL,sample_rate=RATE,chunk_size=CHUNK) as source:
        print("Say somethign...")
        redOn()
        audio = r.listen(source)
        redOff()
    try:
        yellowOn()
        print("Processing...")
        print("We think: " + r.recognize_google(audio))
        yellowOff()
    except sr.UnknownValueError:
        print("google fucked")
        yellowOff()
    except sr.RequestError as e:
        yellowOff()
        print("Your error: {0}".format(e))    

def watchButton():
    while True:
        greenOn()        
        if GPIO.input(BUTTON_ONE) == GPIO.LOW:
            print ("Button Pushed")
            detectSpeech()           
                    

if __name__ == '__main__':
    
    setup()
    try:
        watchButton()
    except KeyboardInterrupt:     
        print("Keyboard Interrupt")
        destroy()              


    
