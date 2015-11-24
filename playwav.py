import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pyaudio
import wave
import sys
import numpy as np
import time
from scipy.io import wavfile
from pylab import*

def fft_info(channel):
	n = len(channel)
	p = fft(channel)
	nUniquePts = ceil((n+1)/2.0)
	p = p[0:nUniquePts]
	p = abs(p)

	p = p / float(n) # scale by the number of points so that
			 # the magnitude does not depend on the length 
			 # of the signal or on its sampling frequency  
	p = p**2  # square it to get the power 

	# multiply by two (see technical document for details)
	# odd nfft excludes Nyquist point
	if n % 2 > 0: # we've got odd number of points fft
	    p[1:len(p)] = p[1:len(p)] * 2
	else:
	    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

	freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n)
	rms_val = sqrt(mean(channel**2))
	return (rms_val, np.amax(10*log10(p)), np.amin(10*log10(p)))

CHUNK = 1024


if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

sampFreq, snd = wavfile.read(sys.argv[1])

wf = wave.open(sys.argv[1], 'rb')
timeArray = np.arange(0,1024,1)
timeArray = timeArray/sampFreq
timeArray = timeArray*1000

ydata = wf.readframes(CHUNK)
decoded = np.fromstring(ydata, snd.dtype)
decoded = decoded / (2.**15)
decoded_left = decoded[::2]
decoded_right = decoded[1::2]
print decoded_left, decoded_right
p = pyaudio.PyAudio()
def update_line(h1, new_data, new_data2):
	h1.set_xdata(np.append(h1.get_xdata(), new_data)) 
	h1.set_ydata(np.append(h1.get_ydata(), new_data2))
	plt.draw()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
plt.ion()
plt.show()
x = np.arange(0,3,1)
while ydata!='':
	ydata = wf.readframes(CHUNK)
	stream.write(ydata)
	decoded = np.fromstring(ydata, 'int16')
	decoded = decoded / (2.**15)
	decoded_left = decoded[::2]
	decoded_right = decoded[1::2]
	left_fft = fft_info(decoded_left)
	right_fft = fft_info(decoded_right)

stream.stop_stream()
stream.close()

p.terminate()
