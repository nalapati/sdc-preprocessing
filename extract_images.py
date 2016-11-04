#!/usr/bin/env python
import cv2
import os
import roslib
import rosbag
import rospy
import sys

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

CAMERA_TIME_FILE = "camera.ts"

def getTime(msg):
  return (msg.header.stamp.secs*1000) + (msg.header.stamp.nsecs/1000000)

def extract_images(bagfile, topicname, outputdir, camera_file, compressed):
  bag = rosbag.Bag(bagfile)
  bridge = CvBridge()
  index = 1
  timestamps = []
  for topic, msg, t in bag.read_messages(topics=[topicname]):
    ti = (getTime(msg) / 50) * 50
    if compressed:
      cv_image = bridge.compressed_imgmsg_to_cv2(msg)
    else:
      cv_image = bridge.imgmsg_to_cv2(msg)
    cv2.imwrite(os.path.join(outputdir, str(index) + ".jpg"), cv_image)
    timestamps.append(ti)
    index = index + 1
  with open(camera_file, "w") as f:
    for ts in timestamps:
      f.write(str(ts))
      f.write("\n")
  bag.close()

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print "python extract_images.py <bagfile path> <topicname> <outputdir to persist images> <compressed>"
    sys.exit()
  bagfile = sys.argv[1]
  topicname = sys.argv[2]
  outputdir = sys.argv[3] 
  os.makedirs(outputdir) 
  compressed = False
  if len(sys.argv) == 5 and sys.argv[4] == 'True':
    compressed=True
  extract_images(bagfile, topicname, outputdir, CAMERA_TIME_FILE, compressed)
  
