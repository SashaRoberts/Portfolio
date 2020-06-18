import pyaudio
import math
import struct
import wave
import time
import os
import numpy as np
import aubio
import multiprocessing

Threshold = 500

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024 * 4
FORMAT = pyaudio.paInt32  # 8
CHANNELS = 1
RATE = 44100
swidth = 2
record_secs = 2

# set pitch defaults
pitch_o = aubio.pitch("default", 1024, 1024 // 2, RATE)
pitch_o.set_unit("Hz")
f_name_directory = 'record'


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):

        print('---Noise detected, recording beginning')
        rec = []

        for ii in range(0, int((RATE / chunk) * record_secs)):
            data = self.stream.read(chunk, exception_on_overflow=False)
            rec.append(data)

        filename = self.write(b''.join(rec))
        pitch = self.get_pitch(filename) / 2
        print("---Finished Recording")
        if 1800 > pitch > 1700:
            print('\nSTART PISTOL DETECTED. WE ARE OFF!')
            return True
        else:
            print('\nReturning to listening')
            return False

    @staticmethod
    def get_pitch(filename):
        src = aubio.source(filename)
        samples, read = src()
        pitch = pitch_o(samples)[0]
        print(f'Pitch: {pitch/2}')
        return pitch

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()

        print('Written to file: {}'.format(filename))

        return filename

    def listen(self):
        print('\nListening for starting noise...')
        starter_pistol = False
        while not starter_pistol:
            input = self.stream.read(chunk, exception_on_overflow=False)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                starter_pistol = self.record()



