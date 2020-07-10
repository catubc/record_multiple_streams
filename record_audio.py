import matplotlib

import numpy as np
import datetime 
import cv2
import time

import nidaqmx
import nidaqmx
from nidaqmx.constants import AcquisitionType
import sys

import matplotlib.pyplot as plt
import PySpin
import simpleaudio as sa

def record_audio(root_dir, duration, start_time):
    import os
    fname_out = os.path.join(root_dir,'audio',start_time+'_audio.npy')
    print ("Saving to: ",fname_out)
    #location = 'animals'
    #sample_time = 60*10  # units = seconds
    s_freq = 250000
    print (s_freq)
    print ("Location: ", root_dir)
    num_samples = duration*s_freq
    dt = 1/s_freq

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai4")

        task.timing.cfg_samp_clk_timing(s_freq,
                                       sample_mode = AcquisitionType.CONTINUOUS)


        data1 = task.read(number_of_samples_per_channel=num_samples, timeout = nidaqmx.constants.WAIT_INFINITELY)

    data1=np.array(data1)
    print (data1.shape)
    np.save(fname_out, data1)

if __name__ == '__main__':
	
	root_dir = sys.argv[1]
	duration = int(sys.argv[2])
	start_time = str(sys.argv[3])
	
	
	record_audio(root_dir, duration, start_time)

