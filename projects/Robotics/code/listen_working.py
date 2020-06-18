import pyaudio
import math
import struct
import wave
import time
import os

Threshold = 40

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
swidth = 2
record_secs = 5

f_name_directory = 'record'


def color_printer(msg):
    try:
        import colorama
        from colorama import Fore, Style
        print(Fore.GREEN + msg + Style.RESET_ALL)
    except Exception as e:
        print(e)
        print(msg)


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

        color_printer('Noise detected, recording beginning')
        rec = []

        for ii in range(0, int((RATE / chunk) * record_secs)):
            data = self.stream.read(chunk, exception_on_overflow=False)
            rec.append(data)

        self.write(b''.join(rec))

        color_printer("finished recording")

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        color_printer('Written to file: {}'.format(filename))
        color_printer('Returning to listening')

    def listen(self):
        color_printer('Listening for audio files...')
        while True:
            input = self.stream.read(chunk, exception_on_overflow=False)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()


def listen_working():
    a = Recorder()
    a.listen()
