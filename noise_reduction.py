import os
import IPython
from scipy.io import wavfile
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import librosa
import warnings
import noisereduce as nr
warnings.filterwarnings("ignore")


def reduce_noise(folder_path, output_path):

    try:
        import noisereduce
    except ImportError as e:
        pass  # module doesn't exist.

    for file in os.scandir(folder_path):

        if file.path.endswith(".wav"):

            _file_path = r"/" + \
                os.path.splitext(os.path.basename(file.path))[0] + ".wav"

            # _file_path = r(folder_path+file_name)
            rate, data = wavfile.read(_file_path)

            # convert audio to float32
            audio = data.astype(np.float32, order='C') / 32768.0

            # Noisy part
            noisy_part = audio[:]

            # select section of data that is noise
            noisy_part = audio[:]

            # perform noise reduction
            reduced_noise = nr.reduce_noise(
                audio_clip=audio, noise_clip=noisy_part, verbose=False)

            scipy.io.wavfile.write(output_path + os.path.splitext(os.path.basename(
                file.path))[0] + "ppa" + ".wav", 48000, reduced_noise)


reduce_noise("/", "output_wav/")
