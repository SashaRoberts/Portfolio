import logging
import os
import time
from pathlib import Path
import time
import sys
from warnings import filterwarnings
filterwarnings("ignore")

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastai import *
from fastai.vision import *
from tqdm import tqdm
import pickle
import multiprocessing


def color_printer(msg):
    try:
        import colorama
        from colorama import Fore, Style
        print(Fore.CYAN + msg + Style.RESET_ALL)
    except Exception as e:
        print(e)
        print(msg)


def convert_master(queue, worker_process, worker_configurer):

    main_path = os.path.dirname(os.path.realpath(__file__))
    audio_path = os.path.join(main_path, "record")
    spectrogram_path = os.path.join(main_path, "spectogram")
    model_path = os.path.join(main_path, "models")

    color_printer('\nLoading in audio detection models...')

    model1 = load_learner(model_path, 'model_1.pkl')
    model2 = load_learner(model_path, 'model_2.pkl')
    model3 = load_learner(model_path, 'model_3.pkl')
    model4 = load_learner(model_path, 'model_4.pkl')
    model5 = load_learner(model_path, 'model_5.pkl')
    model6 = load_learner(model_path, 'model_6.pkl')
    model7 = load_learner(model_path, 'model_7.pkl')
    model8 = load_learner(model_path, 'model_8.pkl')
    model9 = load_learner(model_path, 'model_9.pkl')
    model10 = load_learner(model_path, 'model_10.pkl')

    color_printer('---Audio detection models loaded!')

    index_values = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling', 'gun_shot',
                    'jackhammer', 'siren', 'street_music']

    if not os.path.exists(spectrogram_path):
        os.makedirs(spectrogram_path)

    before = dict([(f, None) for f in os.listdir(audio_path)])

    while True:
        time.sleep(1)
        after = dict([(f, None) for f in os.listdir(audio_path)])
        added = [f for f in after if f not in before]
        removed = [f for f in before if f not in after]
        if added:
            color_printer("Added: ", ", ".join(added))

            # convert files to spectrogram
            for i in tqdm(range(len(added))):
                file = added[i]
                audio_file = audio_path + "//" + file

                samples, sample_rate = librosa.load(audio_file, sr=8000)
                fig = plt.figure(figsize=[0.72, 0.72])
                ax = fig.add_subplot(111)
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                ax.set_frame_on(False)
                filename = spectrogram_path / Path(audio_file).name.replace('.wav', '.png')
                S = librosa.feature.melspectrogram(y=samples, sr=8000)
                librosa.display.specshow(librosa.core.power_to_db(S, ref=np.max))
                plt.savefig(filename, dpi=400, bbox_inches='tight', pad_inches=0)
                plt.close('all')

                color_printer('\n')
                color_printer('Spectrogram Created')

                image = filename

                model1probs = pd.Series(model1.predict(open_image(image))[2], index=index_values, name='model1')
                model2probs = pd.Series(model2.predict(open_image(image))[2], index=index_values, name='model2')
                model3probs = pd.Series(model3.predict(open_image(image))[2], index=index_values, name='model3')
                model4probs = pd.Series(model4.predict(open_image(image))[2], index=index_values, name='model4')
                model5probs = pd.Series(model5.predict(open_image(image))[2], index=index_values, name='model5')
                model6probs = pd.Series(model6.predict(open_image(image))[2], index=index_values, name='model6')
                model7probs = pd.Series(model7.predict(open_image(image))[2], index=index_values, name='model7')
                model8probs = pd.Series(model8.predict(open_image(image))[2], index=index_values, name='model8')
                model9probs = pd.Series(model9.predict(open_image(image))[2], index=index_values, name='model9')
                model10probs = pd.Series(model10.predict(open_image(image))[2], index=index_values, name='model10')

                combined = pd.concat(
                    [model1probs, model2probs, model3probs, model4probs, model5probs, model6probs, model7probs,
                     model8probs, model9probs, model10probs], axis=1)

                class_name = combined.mean(axis=1).idxmax()

                # log detection to gpg.mic
                worker = multiprocessing.Process(target=worker_process,
                                                 args=(queue, 'gpg.mic', class_name, worker_configurer))
                worker.start()
                worker.join()

                color_printer('Prediction:', class_name)

        if removed:
            color_printer("Removed: ", ", ".join(removed))
        before = after
