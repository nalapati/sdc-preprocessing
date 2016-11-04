import multiprocessing
import os
import numpy as np
import shutil
import sys

dataset_1_dir = "/home/ubuntu/datasets/datasets/elcamino"
dataset_2_dir = "/home/ubuntu/datasets/datasets/final_training"
output_dataset_dir = "/home/ubuntu/datasets/datasets/finale"

dataset_1_images_dir = os.path.join(dataset_1_dir, "images")
dataset_1_labels = os.path.join(dataset_1_dir, "labels")
dataset_2_images_dir = os.path.join(dataset_2_dir, "images")
dataset_2_labels = os.path.join(dataset_2_dir, "labels")
output_images_dir = os.path.join(output_dataset_dir, "images")
output_labels = os.path.join(output_dataset_dir, "labels")

index_1 = 0
index_2 = 0
with open(output_labels, "w") as of:
  with open(dataset_1_labels, "r") as df:
    for line in df:
      of.write(line)
      index_1 += 1
  with open(dataset_2_labels, "r") as df:
    for line in df:
      of.write(line)
      index_2 += 1

tasks = []
global_index = 1
for i in range(1, index_1+1):
  tasks.append((os.path.join(dataset_1_images_dir, str(i)+".png.npy"), os.path.join(output_images_dir, str(global_index)+".png.npy")))
  global_index += 1

for i in range(1, index_2+1):
  tasks.append((os.path.join(dataset_2_images_dir, str(i)+".png.npy"), os.path.join(output_images_dir, str(global_index)+".png.npy")))
  global_index += 1

def copy_image(args):
  input_file, output_file = args
  shutil.copyfile(input_file, output_file)
pool = multiprocessing.Pool(8)
pool.map(copy_image, tasks)
