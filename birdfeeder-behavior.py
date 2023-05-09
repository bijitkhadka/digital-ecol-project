from gpiozero import MotionSensor
import logging
from datetime import datetime
from subprocess import call
import picamera
import time
import pygame
import os
import random
import sys
import select
import time

path = "/home/pi/Downloads/project"
all_mp3 = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.mp3')]
#min = 1
#max = 

def rndwav ():
    
        randomfile = random.choice(all_mp3)
        print ("Playing file" ,randomfile,"...")
        
        
        time.sleep(3)#changed from 10 to 3 seconds cause birds only stay for ~5-7seconds.
        pygame.mixer.init()
        pygame.mixer.music.load(randomfile)
       # pygame.mixer.Sound(randomfile).play()
        pygame.mixer.music.play() 
        logging.info('Playing file: '+randomfile+'.mp3')
       # pause = random.randint(min,max)
        #time.sleep(10)
        #print ("Hit key and press enter to stop. Waiting for", pause, "seconds")
        
#the following code is necessary for start up but not after running the first time
#if not os.path.exists('/home/pi/trailcam_log'):
  #  os.makedirs('/home/pi/trailcam_log')

#if not os.path.exists('/home/pi/videos'):
 #   os.makedirs('/home/pi/videos')

#if not os.path.exists('/mnt/usb/videos'):
   # os.makedirs('/mnt/usb/videos')

logfile = "/home/pi/trailcam_log/trailcam_log-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S,')

pir = MotionSensor(4)
duration = 30

print('Starting')
logging.info('Starting')

# Wait an initial duration to allow PIR to settle
print('Waiting for sensor to settle')
time.sleep(1)# changed to from 3 to 1 - 20230422
print('Ready')

while True:
    pir.wait_for_motion()
    logging.info('Motion detected')
    print('Motion detected')
    while pir.motion_detected:
        print('Beginning capture')
        ts = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
        logging.info('Beginning capture: '+ str(ts)+'.h264')
        with picamera.PiCamera() as cam:
            cam.resolution=(1024,768)
            cam.annotate_background = picamera.Color('black')

            cam.start_recording('/home/pi/video.h264')
            start = datetime.now()
            rndwav () # function that plays sounds
            while (datetime.now() - start).seconds < duration:
                cam.annotate_text = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                cam.wait_recording(0.2)
            cam.stop_recording()
        time.sleep(1)
        print('Stopped recording')
        timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
        input_video = "/home/pi/video.h264"

        logging.info('Attempting to save video')
        print('Attempting to save video')

        usb = call("mountpoint -q /mnt/usb", shell=True)

        if usb == 0:
            logging.info('Saving to /mnt/usb/videos/')
            print('Saving to /mnt/usb/videos/')
            output_video = "/mnt/usb/videos/{}.mp4".format(timestamp)
        else:
            logging.info('Saving to /home/pi/videos/')
            print('Saving to /home/pi/videos/')
            output_video = "/home/pi/videos/{}.mp4".format(timestamp)

        call(["MP4Box", "-add", input_video, output_video])
        print('Video ended - sleeping for 3 minutes')
        logging.info('Video ended')
        time.sleep(180)