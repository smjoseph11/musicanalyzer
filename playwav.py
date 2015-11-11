import pyaudio
import wave
import sys
import numpy
import time
from matplotlib import pyplot as plt
from scipy.io import wavfile

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

plt.ion()
sampFreq, snd = wavfile.read(sys.argv[1])

timeArray = numpy.arange(0, 2048.0, 1)
timeArray = timeArray / sampFreq
timeArray = timeArray * 1000
ydata = [0]*timeArray
ax1=plt.axes()

line, = plt.plot(ydata)
plt.ylim([-1,1])
wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)
decoded = numpy.fromstring(data, 'int16')
decoded = decoded / (2.**15)
print decoded
plt.plot(timeArray, decoded, color='k') 
plt.show()
#while data != '':
 #   decoded = numpy.fromstring(data, 'int16')
  #  decoded = decoded / (2.**15)
   # stream.write(data) 
    #data = wf.readframes(CHUNK)
stream.stop_stream()
stream.close()

p.terminate()
