import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import wave
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from pydub import AudioSegment
import os
import subprocess
import tempfile

def generate_srt(spikes, start_time, end_time):
    srt = ''
    for i, spike in enumerate(spikes):
        srt += f"{i+1}\n{start_time+spike[0]} --> {start_time+spike[1]}\n\n"
    return srt


def get_audio_spikes(audio_file):
    # Convert the MP4 file to a WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav') as f:
        os.system(f'ffmpeg -i {audio_file} -y -vn -acodec pcm_s16le -ar 44100 -ac 2 {f.name}')

        # Load the audio data from the WAV file using pydub
        audio = AudioSegment.from_file(f.name, format='wav')

    # Calculate the dBFS for the audio
    dBFS = audio.dBFS

    # Set the minimum length for a spike
    min_silence_len = 1000  # milliseconds
    min_silence_thresh = dBFS - 10

    # Get the audio spikes
    audio_chunks = audio[::1000]
    audio_spikes = []

    print('audio_chnks', audio_chunks)
    for chunk in audio_chunks:
        if chunk.dBFS < min_silence_thresh:
            audio_spikes.append({'start': chunk.start_seconds, 'end': chunk.end_seconds})

    # Convert the audio spikes to a list of dictionaries with start and end timestamps
    spikes = [{'start': spike.start_seconds, 'end': spike.end_seconds} for spike in audio_spikes]

    # Get the start and end times for the audio file
    start_time = spikes[0]['start']
    end_time = spikes[-1]['end']

    return spikes, start_time, end_time