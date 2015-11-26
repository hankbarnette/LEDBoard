#plays an audio file

import pyaudio
import wave
import sys

CHUNK = 8192
DEVICE_CHANNEL = 0

file = 'output.wav'

wf = wave.open(file, 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels = wf.getnchannels(),rate=wf.getframerate(),input_device_index=DEVICE_CHANNEL,output=True)

data = wf.readframes(CHUNK)

print ("Playing...")

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

print ("Done")

stream.stop_stream()
stream.close()

p.terminate()
