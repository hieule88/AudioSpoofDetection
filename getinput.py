import pyaudio
import wave
import numpy as np

#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "./input/input.flac"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
# while(1):
print("Recording")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
spf = wave.open(WAVE_OUTPUT_FILENAME,'r')

# import soundfile as sf

# # Extract audio data and sampling rate from file 
# data, fs = sf.read(WAVE_OUTPUT_FILENAME) 
# # Save as FLAC file at correct sampling rate
# sf.write('./input/myfile.flac', data, fs)  

print('Finish Recording')