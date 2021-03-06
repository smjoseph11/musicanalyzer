import ddf.minim.*;
import ddf.minim.analysis.*;
import javax.swing.JFileChooser;
 
Minim minim;
AudioPlayer song;
FFT fft;

boolean fileSelect = false;
void setup()
{
  size(512, 200);
  selectInput("Select a file to process:", "fileSelected");
  // always start Minim first!
  // specify 512 for the length of the sample buffers
  // the default buffer size is 1024
}
void fileSelected(File selection){
  minim = new Minim(this);
  song = minim.loadFile(selection.getAbsolutePath(), 512);
  song.play();
  // an FFT needs to know how 
  // long the audio buffers it will be analyzing are
  // and also needs to know 
  // the sample rate of the audio it is analyzing
  fft = new FFT(song.bufferSize(), song.sampleRate());
    fileSelect = true;
}
 
void draw()
{
  if(fileSelect){
  background(0);
  // first perform a forward fft on one of song's buffers
  // I'm using the mix buffer
  //  but you can use any one you like
  fft.forward(song.mix);
 
  stroke(510, 0, 0, 256);
  // draw the spectrum as a series of vertical lines
  // I multiple the value of getBand by 4 
  // so that we can see the lines better
  for(int i = 0; i < fft.specSize(); i++)
  {
    line(i, height, i, height - fft.getBand(i)*8);
  }
 
  stroke(255);
  // I draw the waveform by connecting 
  // neighbor values with a line. I multiply 
  // each of the values by 50 
  // because the values in the buffers are normalized
  // this means that they have values between -1 and 1. 
  // If we don't scale them up our waveform 
  // will look more or less like a straight line.
  for(int i = 0; i < song.left.size() - 1; i++)
  {
    line(i, 50 + song.left.get(i)*50, i+1, 50 + song.left.get(i+1)*50);
    line(i, 150 + song.right.get(i)*50, i+1, 150 + song.right.get(i+1)*50);
  }
  }
}