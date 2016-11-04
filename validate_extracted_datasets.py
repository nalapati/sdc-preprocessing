import os

root_dir = "/home/ubuntu/datasets/new_datasets"
for f in os.listdir(root_dir):
  print f
  print len(os.listdir(os.path.join(root_dir, f, "images")))
  with open(os.path.join(root_dir, f, "labels")) as fil:
    print len(fil.readlines())
