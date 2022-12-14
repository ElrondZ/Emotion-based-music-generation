import wave
import pyaudio
import struct
from math import cos, sin, pi
import tkinter as Tk
from tkinter import HORIZONTAL

def fun_quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False

def fun_sinusoidal():
    global MODE
    MODE = "sin"

def fun_triangle():
    global MODE
    MODE = "triangle"

Fs = 8000
gain = 0.2 * 2 ** 15
MODE = 'sin'

# Define the range of the minimum and maximum frequency respectively
FREQUENCY_MIN_LEFT = 0
FREQUENCY_MIN_RIGHT = 500
FREQUENCY_MAX_LEFT = 500
FREQUENCY_MAX_RIGHT = 1000

# Define the time it takes for the siren sound to repeat (cycle time) and the range
CYCLE_TIME = 5
CYCLE_TIME_MIN = 1
CYCLE_TIME_MAX = 10

# Define Tkinter root
root = Tk.Tk()

# Define and Initialize Tk variables
freq_max = Tk.DoubleVar()
freq_min = Tk.DoubleVar()
T = Tk.DoubleVar()
freq_max.set(FREQUENCY_MAX_LEFT)
freq_min.set(FREQUENCY_MIN_LEFT)
T.set(CYCLE_TIME)

# Define widgets
freq1 = Tk.Scale(root, label='Maximum Frequency', variable=freq_max, from_=FREQUENCY_MAX_LEFT, to=FREQUENCY_MAX_RIGHT, length=300, orient=HORIZONTAL, tickinterval=100)
freq2 = Tk.Scale(root, label='Minimum Frequency', variable=freq_min, from_=FREQUENCY_MIN_LEFT, to=FREQUENCY_MIN_RIGHT, length=300, orient=HORIZONTAL, tickinterval=100)
cycle_time = Tk.Scale(root, label='Cycle Time', variable=T, from_=CYCLE_TIME_MIN, to=CYCLE_TIME_MAX, length=300, orient=HORIZONTAL, tickinterval=1)
B_sinusoidal = Tk.Button(root, text='Play sinusoidal', command=fun_sinusoidal)
B_triangle = Tk.Button(root, text='Play triangle', command=fun_triangle)
B_quit = Tk.Button(root, text='Quit', command=fun_quit)

# Place widgets
B_quit.pack(side=Tk.BOTTOM, fill=Tk.X)
B_sinusoidal.pack(side=Tk.BOTTOM, fill=Tk.X)
B_triangle.pack(side=Tk.BOTTOM, fill=Tk.X)
cycle_time.pack(side=Tk.BOTTOM)
freq1.pack(side=Tk.BOTTOM)
freq2.pack(side=Tk.BOTTOM)

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=Fs,
    input=False,
    output=True,
    frames_per_buffer=128)

#save the output
wb = wave.open('output_file.wav', 'wb')
wb.setnchannels(1)
wb.setsampwidth(2)
wb.setframerate(Fs)

BLOCKLEN = 256
output_block = [0] * BLOCKLEN
f = [0] * BLOCKLEN
theta1 = 0
theta2 = 0
theta = 0
CONTINUE = True

while CONTINUE:
    root.update()
    # freq_mid is the middle value of maximum and minimum frequencies
    freq_mid = (freq_max.get() + freq_min.get()) / 2
    # diff is the range of maximum and minimum frequencies
    diff = freq_max.get() - freq_min.get()
    om1 = 2.0 * pi / (T.get() * Fs)

    if MODE == 'sin':
        for i in range(0, BLOCKLEN):
            # sin(theta1)) ranges from -1 to 1,
            # so freq_mid + diff / 2 * (sin(theta1)) ranges from freq_min to freq_max
            om2 = 2.0 * pi * int(freq_mid + diff / 2 * sin(theta1)) / Fs
            output_block[i] = int(gain * sin(theta2))
            theta1 = theta1 + om1
            theta2 = theta2 + om2
        if theta1 > pi:
            theta1 = theta1 - 2.0 * pi
        if theta2 > pi:
            theta2 = theta2 - 2.0 * pi

        binary_data = struct.pack('h' * BLOCKLEN, *output_block)  # 'h' for 16 bits
        stream.write(binary_data)
        wb.writeframes(binary_data)

    elif MODE == 'triangle':
        for i in range(0, BLOCKLEN):
            if theta1 >0:
                om2 = 2.0 * pi * int(freq_mid + (diff / 2) * (2 * theta1 / pi - 1)) / Fs
            else:
                om2 = 2.0 * pi * int(freq_mid + (diff / 2) * (-2 * theta1 / pi - 1)) / Fs
            output_block[i] = int(gain * sin(theta2))
            theta1 = theta1 + om1
            theta2 = theta2 + om2
        if theta1 > pi:
            theta1 = theta1 - 2.0 * pi
        if theta2 > pi:
            theta2 = theta2 - 2.0 * pi

        binary_data = struct.pack('h' * BLOCKLEN, *output_block)  # 'h' for 16 bits
        stream.write(binary_data)
        wb.writeframes(binary_data)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()