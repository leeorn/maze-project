#!/usr/bin/env python
import numpy as np
import cv2
from libfreenect.wrappers.python import frame_convert2
import freenect
import os
import csv

# this shows the video from the Kinect
def get_video():
    return freenect.sync_get_video()[0]

def main():

    while 1:
        rgb_img = frame_convert2.video_cv(get_video())
        rgb_csv = get_video()
        cv2.imshow('Video', rgb_img)

        if cv2.waitKey(1) == 112: # if clicked 'p' 
            break
    
    print('Picutre was taken')
            
    #path = os.getcwd()
    path = '~/Desktop/maze-project'
    img_file_name = 'maze_pic.jpeg'
    csv_file_name = 'maze_csv.csv'

    # change to correct dir
    #os.chdir(path)

    # write the img
    cv2.imwrite(img_file_name, rgb_img)

    # create csv file
    print('write CSV file')
    with open(csv_file_name, 'w+') as csv_file:
        file_writer = csv.writer(csv_file, delimiter = ',')
        for i in range(len(rgb_csv)):
            file_writer.writerow(rgb_csv[i])



if __name__ == '__main__':
    main()
    print('Done!')




