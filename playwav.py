import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pyaudio
import wave
import sys
import numpy as np
import time
from scipy.io import wavfile

CHUNK = 1024


if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

sampFreq, snd = wavfile.read(sys.argv[1])

wf = wave.open(sys.argv[1], 'rb')

ydata = wf.readframes(CHUNK)
decoded = np.fromstring(ydata, snd.dtype)
decoded = decoded / (2.**15)
decoded_left = decoded[::2]
decoded_right = decoded[1::2]
print decoded_left, decoded_right
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

while ydata!='':
	ydata = wf.readframes(CHUNK)
	stream.write(ydata)
	decoded = np.fromstring(ydata, 'int16')
	decoded = decoded / (2.**15)
	decoded_left = decoded[::2]
	decoded_right = decoded[1::2]
	print decoded_left
	print decoded_right
stream.stop_stream()
stream.close()

p.terminate()
