#Test Run of Speech Recognition

import speech_recognition as sr

CHUNK = 8192
CHANNELS = 1
RATE = 44100
DEVICE_CHANNEL = 2

r = sr.Recognizer()
r.energy_threshold = 3000
with sr.Microphone(device_index=DEVICE_CHANNEL,sample_rate=RATE,chunk_size=CHUNK) as source:
    print("Say somethign...")
    audio = r.listen(source)

try:

    print("We think: " + r.recognize_google(audio))

except sr.UnknownValueError:
    print("google fucked")

except sr.RequestError as e:
    print("Your error: {0}".format(e))
