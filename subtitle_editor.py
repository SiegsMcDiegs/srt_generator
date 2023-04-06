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


class SubtitleEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.audio_file = 'example.wav'

        # Create a canvas for the waveform plot
        self.figure = plt.Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Create a button to display the waveform
        self.display_button = tk.Button(self.root, text='Display Waveform', command=self.display_waveform)
        self.display_button.pack()

        # Create an "Open" button to select a file
        self.open_button = tk.Button(self.root, text='Open', command=self.open_file)
        self.open_button.pack()

    def display_waveform(self):
        # Convert the MP4 file to a WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            os.system(f'ffmpeg -i {self.audio_file} -y -vn -acodec pcm_s16le -ar 44100 -ac 2 {f.name}')
            # Load the audio data from the WAV file using wave
            with wave.open(f.name, 'rb') as wf:
                audio = wf.readframes(wf.getnframes())

        # Convert the audio data to a numpy array
        audio = np.frombuffer(audio, dtype=np.int16)

        # Plot the audio waveform
        self.figure.clear()
        plt.plot(audio)
        plt.show()
        self.canvas.draw()



    def open_file(self):
        # Display a file dialog window and get the selected file
        filetypes = [('MP4 Files', '*.mp4')]
        file_path = filedialog.askopenfilename(title='Open', filetypes=filetypes)

        # Set the audio file and update the display
        if file_path:
            self.audio_file = file_path
            self.display_waveform()

    def convert_to_wav(input_file, overwrite_output=False):
        output_file = os.path.splitext(input_file)[0] + '.wav'
        if not overwrite_output and os.path.isfile(output_file):
            print(f'Error: {output_file} already exists')
            return

        command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', '-y', output_file]
        subprocess.run(command, check=True)
        
        return output_file



    def run(self):
        self.root.mainloop()



if __name__ == '__main__':
    editor = SubtitleEditor()
    editor.run()