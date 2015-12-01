#Test network copy
import shutil

messageFile = '/home/pi/Desktop/Python/LEDSpeech/testNetwork.txt'
remoteFilePath = '/LEDSIGN'




shutil.copy(messageFile,remoteFilePath)


