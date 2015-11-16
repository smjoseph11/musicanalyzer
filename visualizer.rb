#visualizer.rb

class Visualizer < Processing::App
	load_library "minim"
	import "ddf.minim"
	import "ddf.minim.analysis"

	def setup
		smooth # smoother == prettier
		size(1280,100) #let's pick a more interesting size
		background 10 #... and a darker background color
		setup_sound
	end

	def draw
	
	end
	
	def setup_sound
		#Creates a Minim object	
		@minim = Minim.new(self)
		#Lets Minim grab sound data from mic
		@input = @minim.get_line_in
		#Gets FFT values from sound data
		@fft = FFT.new(@input.left.size, 44100)
		#beat detection
		@beat = BeatDetect.new
		
		@freqs = [60, 170, 310, 600, 1000, 3000, 6000, 12000, 1400, 16000]
		@current_ffts = Array.new(@freqs.size, 0.001)
		@previous_ffts = Array.new(@freqs.size, 0.001)
		@max_ffts = Array.new(@freqs.size, 0.001)
		@scaled_ffts = Array.new(@freqs.size, 0.001)
		
		#smoothing
		@fft_smoothing = 0.8	

	end
	def update_sound
		@fft.forward(@input.left)
		@previous_ffts = @current_ffts
		#Iterate over the frequencies of interst and get FFT values
		@freqs.each_with_index do |freq, i|
		#the FFT value for this frequency
		new_fft = @fft.get_freq(freq)
		
		#Set it as the frequency max if it's larger than the previous max
		@max_ffts[i] = new_fft if new_fft > @max_ffts[i]

		#Use our "smoothness" factor and the previous FFT to set a current FFT value
		@current_ffts[i] = ((1-@fft_smoothing) *  new_fft) + (@fft_smoothing * previous_ffts[i])
		#set a scaled/normalized FFT value that will be easier to work with
		
		@scaled_ffts[i] = (@current_ffts[i]/@max_ffts[i])
	end
	@beat.detect(@input.left)
end

Visualizer.new :title => "Visualizer"
