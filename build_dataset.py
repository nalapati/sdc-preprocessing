import cv2
import multiprocessing
import numpy as np
import os

def process_final_image(args):
    src_path, dest_dir, image_index, flipped_image_index = args
    normal_path = os.path.join(dest_dir, '%d.png.npy' % image_index)
    flipped_path = os.path.join(dest_dir, '%d.png.npy' % flipped_image_index)
    print src_path
    cv_image = cv2.imread(src_path)
    cv_image = cv2.resize(cv_image, (320, 240))
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
    cv_image = cv_image[120:240, :, :]

    np.save(normal_path, cv_image)

    # flip the image over the y axis to equalize left/right turns
    cv_image = cv_image[:, ::-1, :]
    np.save(flipped_path, cv_image)

dataset_path = "/home/ubuntu/datasets/new_datasets"
dest_dir = "/home/ubuntu/datasets/datasets/elcamino"
dest_image_dir = os.path.join(dest_dir, "images")
if not os.path.exists(dest_image_dir):
  os.makedirs(dest_image_dir)
dest_labels_file = os.path.join(dest_dir, "labels")
bagdirs = [] 
for bagdir in os.listdir(dataset_path):
  bagdirs.append(os.path.join(dataset_path, bagdir))

bagdirs.sort()

tasks = []
labels = []
index = 1

for bagdir_path in bagdirs:
  print "processing labels %s" % bagdir_path
  with open(os.path.join(bagdir_path, "labels"), "r") as f:
    bag_labels = f.readlines()
  labels.extend(bag_labels)

for bagdir_path in bagdirs:
  print "processing %s" % bagdir_path
  with open(os.path.join(bagdir_path, "labels"), "r") as f:
    length = len(f.readlines())
  for i in range(1, length+1):
    tasks.append((os.path.join(bagdir_path, "images", str(i)+".jpg"), dest_image_dir, index, len(labels)+index))
    index = index + 1

with open(dest_labels_file, "w") as f:
  for label in labels:
    f.write(label.strip())
    f.write("\n") 
  for label in labels:
    f.write(str(-float(label.strip())))
    f.write("\n")
#pool = multiprocessing.Pool(8)
#pool.map(process_final_image, tasks)
print "done"
