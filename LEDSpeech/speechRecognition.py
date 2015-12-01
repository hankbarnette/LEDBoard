#Speech Reconition for LED Marquee

#The Real Deal

#Lots of imports
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import speech_recognition as sr

import httplib2
import os

from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload

import oauth2client
from oauth2client import client
from oauth2client import tools


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
SPEECH_THRESHOLD = 2000

#Define LEDs
LED_GREEN = GPIO1
LED_YELLOW = GPIO2
LED_RED = GPIO3
BUTTON_ONE = GPIO0

#File Setups
USE_GOOGLE_DRIVE = true
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = '/home/pi/Desktop/Credentials/client_secret.json'
APPLICATION_NAME = 'Speech Recognition LED Board'
messageFile = '/home/pi/Desktop/Python/LEDSpeech/spokenMessages.txt'
messageFileTitle = 'spokenMessages.txt'
messageFileID = '0B_c8EUKFDVmpLUtDNjJzOEJXcDA'
messageFileDescription = 'Messages Spoken via Raspberry PI'
messageFileMIMETYPE = 'text/plain'
LEDFolderID = '0B_c8EUKFDVmpTW1HZ1dLRFpla0E'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'SpeechRecognition.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def updateFileDRIVE(service, file_id, new_title, new_description, new_mime_type, new_filename, new_revision):

    try:
        print('Uploading file to DRIVE: %s' % new_title)
        #Get the file to update
        file = service.files().get(fileId=file_id).execute()

        #update metadata
        file['title'] = new_title
        file['description'] = new_description
        file['mimeType'] = new_mime_type

        #File Content
        media_body = MediaFileUpload(new_filename,mimetype=new_mime_type,resumable=True)

        #Send the request
        updated_file = service.files().update(fileId=file_id,body=file,newRevision=new_revision,media_body=media_body).execute()

        return updated_file
    except errors.HttpError as error:
        print ('Update error occured: %s' % error)
        return None

#setup drive
def setupDrive():
    print("Setting up DRIVE...")
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service

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
    r.energy_threshold = SPEECH_THRESHOLD
    #Turn off Greed LED
    greenOff()
    
    with sr.Microphone(device_index=DEVICE_CHANNEL,sample_rate=RATE,chunk_size=CHUNK) as source:
        print("Calibrating...")
        r.adjust_for_ambient_noise(source,duration=1)
        print("Waiting for speech...")
        redOn()
        audio = r.listen(source)
        redOff()
    try:
        yellowOn()
        print("Processing...")
        text = r.recognize_google(audio)
        #print("We think: " + text)        
        #yellowOff()      
    except sr.UnknownValueError:
        #print("google fucked")
        #yellowOff()
        text = "What did you say?"
    except sr.RequestError as e:
        #yellowOff()
        #print("Your error: {0}".format(e))
        text = "Google Error"

    #print("left try")
    return text

def watchButton():
    while True:
        greenOn()        
        if GPIO.input(BUTTON_ONE) == GPIO.LOW:
            print ("---Button pushed---")
            processText(detectSpeech())

def updateFileNetwork(file)
    print("Uploading file to NETWORK: %s" % file)
    


def processText(text):
    print("You said: %s" % text)

    #Write the local file
    with open(messageFile,'w') as f:
        f.write(text)

    #Upload the file
    if USE_GOOGLE_DRIVE:
        service = setupDrive()
        updateFileDRIVE(service,messageFileID,messageFileTitle,messageFileDescription,messageFileMIMETYPE,messageFile,0)
    else
        updateFileNetwork(messageFile)

    #Turn off Light
    yellowOff()

if __name__ == '__main__':
    
    setup()
    
    try:
        print("Starting...")
        watchButton()
    except KeyboardInterrupt:     
        print("Keyboard Interrupt")
        destroy()              
    
