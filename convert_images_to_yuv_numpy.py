#!/usr/bin/env python
import numpy as np
import os
import rosbag
import roslib
import rospy
import sys
import cv2

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def convert(input_image_dir, output_image_dir, padding):
  for f in os.listdir(input_image_dir):
    cv_image = cv2.imread(os.path.join(input_image_dir, f))
    img_out = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
    if padding:
      padding_rows = img_out.shape[1] - img_out.shape[0]
      np.save(
          os.path.join(output_image_dir, f), 
          np.pad(cv_image, pad_width=((padding_rows/2, padding_rows/2), (0,0), (0, 0)), mode='constant', constant_values=0))
    else:
      np.save(os.path.join(output_image_dir, f), cv_image)

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print 'python convert_images_to_yuv_numpy.py <input image directory> <output image directory> <padding>'
  input_image_dir = sys.argv[1]
  output_image_dir = sys.argv[2]
  padding = False
  if len(sys.argv) == 4 and sys.argv[3] == 'True':
    padding = True
  convert(input_image_dir, output_image_dir, padding)

