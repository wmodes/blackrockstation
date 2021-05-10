import pyaudio
import pydub

file = "data/stereo-test.mp3"

pyaudio.player = Sound()
pyaudio.player.read(file)
pyaudio.player.play()
