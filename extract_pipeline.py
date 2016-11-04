import os
import shutil
import subprocess
import sys

from extract_images import extract_images
from extract_steering_angles import extract
from extract_vehicle_speed import extract_speed

def extract_val_for_ts(ts_to_val, ts):
  if ts in ts_to_val:
    return ts_to_val[ts]
  else:
    offsets = [50, 100, 150, -50, -100, -150]
    for offset in offsets:
      if ts + offset in ts_to_val:
        return ts_to_val[ts + offset]

def extract_images_labels(image_dir_path, image_ts_path, steering_ts_path, speed_ts_path, labels_path, image_path):
  with open(image_ts_path, "r") as f:
    cc_ts = f.readlines()

  with open(steering_ts_path, "r") as f:
    ts_sa = f.readlines()
  
  with open(speed_ts_path, "r") as f:
    ts_sp = f.readlines()

  ts_to_sa = {}
  for line in ts_sa:
    parts = line.split(" ")
    ts_to_sa[int(parts[0])] = float(parts[1])

  ts_to_sp = {}
  for line in ts_sp:
    parts = line.split(" ")
    ts_to_sp[int(parts[0])] = float(parts[1])

  with open(labels_path, "wb") as f:
    index=1
    new_index = 1
    for ts in cc_ts:
      ts = int(ts.strip())
      sa = extract_val_for_ts(ts_to_sa, ts)
      sp = extract_val_for_ts(ts_to_sp, ts)
      if (sa is not None) and (sp is not None) and (sp > 0.0005):
        f.write(str(sa))
        f.write('\n') 
        shutil.copyfile(os.path.join(image_dir_path, str(index)+".jpg"), os.path.join(image_path, str(new_index)+".jpg"))
        new_index += 1
      index += 1

def extract_images_and_steering(bagfile, output_dir):
  output_path = os.path.join(output_dir, os.path.basename(bagfile))
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  
  image_dir_path = os.path.join(output_path, "images-staging")
  if not os.path.exists(image_dir_path):
    os.makedirs(image_dir_path)
  image_ts_path = os.path.join(output_path, "camera.ts")
  steering_ts_path = os.path.join(output_path, "steering.ts")
  speed_ts_path = os.path.join(output_path, "speed.ts")
  labels_path = os.path.join(output_path, "labels")
  image_path = os.path.join(output_path, "images")
  if not os.path.exists(image_path):
    os.makedirs(image_path)

  print "extracting images for %s" % (bagfile)
  extract_images(bagfile, "/left_camera/image_color/compressed", image_dir_path, image_ts_path, True)
  print "extracting steering for %s" % (bagfile)
  extract(bagfile, "/vehicle/steering_report", steering_ts_path)
  print "extracting speed for %s" % (bagfile)
  extract_speed(bagfile, "/vehicle/wheel_speed_report", speed_ts_path)
  print "extracting labels for %s" % (bagfile)
  extract_images_labels(image_dir_path, image_ts_path, steering_ts_path, speed_ts_path, labels_path, image_path)
  print "done with %s" % (bagfile)

for f in os.listdir('/home/ubuntu/Downloads/Ch2-Train/'):
  extract_images_and_steering(os.path.join('/home/ubuntu/Downloads/Ch2-Train', f), '/home/ubuntu/datasets/new_datasets')
print "done!!"

