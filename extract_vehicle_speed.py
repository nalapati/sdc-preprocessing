#!/usr/bin/env python
import rosbag
import sys

SPEED_FILE = "speed.ts"

def getTime(msg):
  return (msg.header.stamp.secs * 1000) + (msg.header.stamp.nsecs / 1000000)

def extract_speed_from_msg(msg):
  max_rad_s = max(msg.front_left, msg.front_right, msg.rear_left, msg.rear_right)
  revs_s = max_rad_s / (3.14 *2)
  inches_s = revs_s * 3.14 * 26.7
  miles_s = inches_s / 63360.0

  return miles_s

def extract_speed(bagfile, topic, speed_file):
  bag = rosbag.Bag(bagfile)
  prev = 0
  with open(speed_file, "w") as f:
    for topic, msg, t in bag.read_messages(topics=[topic]):
      ts = (getTime(msg) / 50) * 50
      if ts <> prev:
        f.write(str(ts) + " " + str(extract_speed_from_msg(msg)))
        f.write("\n")
        prev = ts
  bag.close()

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print 'python extract_vehicle_speed.py <bag file> <topic>'
    sys.exit()
  bagfile = sys.argv[1]
  topic = sys.argv[2]
  extract(bagfile, topic, SPEED_FILE)

