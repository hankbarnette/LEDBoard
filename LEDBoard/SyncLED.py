import os
import win32file
import win32event
import win32con
import time
import alphasign

#message file paths
#messageFile = "F:\\Personal\\Google Drive\\LEDSIGN\\messages.txt"
messageFile = "F:\\Personal\\Google Drive\\LEDSIGN\\messages.txt"
messagePath = "F:\\Personal\\Google Drive\\LEDSIGN\\"



def watchFile():

    #setup the notifciation
    watchNotification = win32file.FindFirstChangeNotification(messagePath,0,win32con.FILE_NOTIFY_CHANGE_SIZE)

    try:
        while 1:
            #print "Watching"            
            result = win32event.WaitForSingleObject(watchNotification, 500)
                        
            #If there was a change
            if result == win32con.WAIT_OBJECT_0:                

                #Read the message file
                readMessages(messageFile)                

                #Start watching again for next notification
                win32file.FindNextChangeNotification (watchNotification)                
    finally:
        #close it all down
        print "Closing the notification watch"
        win32file.FindCloseChangeNotification (watchNotification)



def readMessages(file):

    print "=========================="
    print "READING NEW MESSAGES"
    print "=========================="

    #read the message file
    with open(file) as f:
        messagesList = f.read().splitlines()

    #update the sign
    updateLED(messagesList)



###updates the LED display        
##def updateLED(list):
##  
##    sign = alphasign.Serial(0)
##    sign.connect()
##    print "Clearing sign memory"
##    sign.clear_memory()
##    
##    # create logical objects to work with
##    counter_str = alphasign.String(label="1")
##    signText = alphasign.Text(label="A")
##     
##    # allocate memory for these objects on the sign
##    print "Allocating sign text"
##    sign.allocate((signText,))
##
##    #Loop through messages
##    for message in list:
##        print "Writing: %s" % message
##        message = "     " + message + "     "
##        signText.data = message
##        sign.write(signText)
##        print "Waiting"
##        time.sleep(5)


#updates the LED display        
def updateLED(list):
  
    sign = alphasign.Serial(0)
    sign.connect()
    print "Clearing sign memory"
    #sign.clear_memory()
    #sign.beep(frequency=0,duration=0.1,repeat=0)
    

    #create the sequence
    messages = []
    for position, item in enumerate(list):
        messageData = item
        #cleanup the message a bit
        #messageData = "%s" + "        " + messageData + "        "
        messageData = "%s" + messageData

        
        label = position + 1
        messageText = alphasign.Text((messageData % alphasign.charsets.TEN_HIGH_STD),label=str(label),mode=checkMode(messageData),position=checkPosition(messageData))
        #messageText = alphasign.Text(messageData % alphasign.charsets.SEVEN_SHADOW,label=str(label))
        #messageText = alphasign.Text((messageData % alphasign.charsets.SEVEN_HIGH_FANCY),label="A")
        print "Message Data: %s" % messageData
        print str(position)
        print "Position: %s" % position
        
        messages.append(messageText)        
     
    # allocate memory for these objects on the sign
    print "Allocating sign text"    
    sign.allocate((messages))
    #print "Updating Sequence"
    #sign.set_run_sequence((messages))
    print "Writing messages"
    for obj in (messages):
        sign.write(obj)


def checkMode(message):

    #Big else if for all modes
    if "fireworks" in message:
        mode = alphasign.modes.FIREWORKS
    elif "thank you" in message:
        mode = alphasign.modes.THANK_YOU
    elif "no smoking" in message:
        mode = alphasign.modes.NO_SMOKING
    elif "running animal" in message:
        mode = alphasign.modes.RUNNING_ANIMAL
    elif "fish animation" in message:
        mode = alphasign.modes.FISH_ANIMATION
    elif "don't drink and drive" in message:
        mode = alphasign.modes.DONT_DRINK_DRIVE
    elif "turbo car" in message:
        mode = alphasign.modes.TURBO_CAR
    elif "ballon animation" in message:
        mode = alphasign.modes.BALLOON_ANIMATION
    elif "cherry bomb" in message:
        mode = alphasign.modes.CHERRY_BOMB
    elif "trumpet" in message:
        mode = alphasign.modes.TRUMPET_ANIMATION        
    else:
        mode = alphasign.modes.ROLL_UP
    return mode

def checkPosition(message):
    #check position of text on screen    
    if "top row" in message:
        position = alphasign.positions.TOP_LINE
    elif "bottom row" in message:
        position = alphasign.positions.BOTTOM_LINE
    else:
        position = alphasign.positions.MIDDLE_LINE

    return position
 

#=======MAIN===========

print "--------Sync LED Starting--------"

watchFile()
    
