import IPython
from scipy.io import wavfile
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import librosa

# wav_loc = "harshit_slow.wav"
wav_loc = "download.wav"
rate, data = wavfile.read(wav_loc)
# data = data / 32768
IPython.display.Audio(data=data, rate=rate)
fig, ax = plt.subplots(figsize=(20, 4))
ax.plot(data)
