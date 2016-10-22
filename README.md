# sdc-preprocessing

## Requirements
```
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116
sudo apt-get update
sudo apt-get install ros-indigo-desktop-full
sudo rosdep init
rosdep update
sudo apt-get install python-rosinstall
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc
roscd image_view
rosmake image_view --rosdep-install
sudo aptitude install mjpegtools
```

## Listing topics in a bag file
```
rosbag info dataset.bag
```
