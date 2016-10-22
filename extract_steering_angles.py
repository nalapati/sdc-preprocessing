#!/usr/bin/env python
import rosbag
import sys

def getTime(msg):
  return (msg.header.stamp.secs * 1000) + (msg.header.stamp.nsecs / 1000000)

def extract(bagfile, topic):
  bag = rosbag.Bag(bagfile)
  prev = 0
  for topic, msg, t in bag.read_messages(topics=[topic]):
    ts = (getTime(msg) / 50) * 50
    if ts <> prev:
      print str(ts) + " " + str(msg.steering_wheel_angle)
      prev = ts
  bag.close()

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print 'python extract_steering_angles.py <bag file> <topic>'
    sys.exit()
  bagfile = sys.argv[1]
  topic = sys.argv[2]
  extract(bagfile, topic)

