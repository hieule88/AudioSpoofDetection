import pyaudio
import wave
import numpy as np
from math import log10
import audioop  
import time

#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
WIDTH = 2
FORMAT = pyaudio.paInt16
p = pyaudio.PyAudio()

rms = 0
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


stream = p.open(format=FORMAT,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

while stream.is_active(): 
    db = 20 * log10(rms)
    print(f"RMS: {rms} DB: {db}") 
    # refresh every 0.3 seconds 
    time.sleep(0.3)

stream.stop_stream()
stream.close()

p.terminate()