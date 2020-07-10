import matplotlib


import numpy as np
import datetime 
import cv2
import time

import nidaqmx
import nidaqmx
from nidaqmx.constants import AcquisitionType

import PySpin

import sys

def setup_camera():
    
    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, 
                                            version.type, version.build))
    
    
    return system

def setup2(system, FPS, duration, epochs):
    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()
    cam = cam_list[0]

    # Retrieve TL device nodemap and print device information
    nodemap_tldevice = cam.GetTLDeviceNodeMap()

    # Initialize camera
    cam.Init()

    # Retrieve GenICam nodemap
    nodemap = cam.GetNodeMap()

    # Acquire images
    #acquire_images(cam, nodemap, nodemap_tldevice)

    node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))

    node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')

    acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

    # set the frame rate manually
    cam.AcquisitionFrameRateEnable.SetValue(True)
    cam.AcquisitionFrameRate.SetValue(FPS)

    # check frame rate is correct
    node_acquisition_framerate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
    framerate_to_set = node_acquisition_framerate.GetValue()
    print ("Frame rate to be set to %dFPS" % framerate_to_set)

    # Set integer value from entry node as new value of enumeration node
    node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

    # set default saving directory

    # set opencv recorder parameters
    height, width, layers = [1280,1024,3]
    size= (height, width)

    # avi compression option
    option = PySpin.H264Option()
    option.frameRate = int(framerate_to_set)
    option.bitrate = 5000000
    option.height = 1024
    option.width = 1280
    
    print ("DONE SETUP CAMERA")
    
    return cam, option, size
    
# record video    
def record_video(root_dir, system, FPS, cam, option, size, start_time):
    import cv2, os
    from dateutil import tz
    UTC = tz.gettz('UTC')

    print ("STARTING SETUP RECORDING")
    try: 
        cam.EndAcquisition()
    except:
        pass



    for epoch in epochs:
        print ("starting epoch: ", epoch)
        # initialize time stamps for camera
        times=[]

        # start a new video file
        cv2_file = os.path.join(root_dir,'video',start_time+'.avi')
        out = cv2.VideoWriter(cv2_file,cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)

        # start video acquisition and grab individual video files
        cam.BeginAcquisition()

        # grab individual video frames
        for k in range(int(option.frameRate)*duration):

            image_result = cam.GetNextImage()
            
            time = image_result.GetTimeStamp()

            times.append(time)
            if k%100==0:
                print("Frame: ", k, "start_time: ", time)

            # convert image to bgr for saving
            images_avi = image_result.Convert(PySpin.PixelFormat_BGR8)

            # add image to opencv avi file
            out.write(images_avi.GetData().reshape((1024, 1280, 3)))

            # release iamge
            image_result.Release()

        # close the video recording
        out.release()

        # close the camera
        cam.EndAcquisition()
                
        np.savetxt(os.path.join(root_dir,'times',start_time+'_frame_times.txt'),times, fmt="%s")


if __name__ == '__main__':
	# initialize recordings recording
	root_dir = r"E:\july_8_gerbil2"

	root_dir = sys.argv[1]
	duration = int(sys.argv[2])
	start_time = str(sys.argv[3])


	FPS = int(25)
	#duration = 10
	epochs = [0]

	# setup camera stage 1
	system = setup_camera()

	# setup camera stage 2
	cam, option, size  = setup2(system, FPS, duration, epochs)

	# record video
	record_video(root_dir, system, FPS, cam, option, size, start_time)
