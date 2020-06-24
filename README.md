# Clearbot Jetson Nano Codebase

### Requirements

- OpenCV (latest version from the repo: see setup instructions for details)
- Git and Git LFS (LFS is used for weights file)
- Python 3.6 or above

##### When cloning this repository, make sure that you have Git LFS to pull the weights file. Otherwise you will get an error on running the code.

### How to setup and run this code?

Make sure that OpenCV has been compiled and installed.

##### Note ( 19th June, 2020): OpenCV needs to be compiled because the YOLOv4 requires features that are scheduled in a future release. [Track the issue here](https://github.com/opencv/opencv/pull/17185)

#### Creating a virtual environment for the project

A python 3 virtual environment can be created as follows:

```bash
pip install virtualenv --user
virtualenv .venv -p python3
source .venv/bin/activate
```

#### Installing OpenCV that has been built on the machine, to the virtual environment

Make sure that you have compiled OpenCV using the command `make`. You DO NOT need to run `make install` for this to work.

Also make sure that you installed a Python virtual environment for this project.

Let us assume that the path to the `opencv/build` directory is `$OPENCV`

```bash
cd .venv/lib/python3.8/site-packages
ln -s $OPENCV/lib/python3/cv2.cpython-38-darwin.so cv2.so
```

The above file names, or the Python version may be slightly different for you. Make sure you use the correct version while using the commands above.

Now, for the last step, make sure that you have `.venv` active using the command: `source .venv/bin/activate`. Then try to see if you have configured OpenCV correctly:

```python
>> import cv2
>> cv2.__version__
```

If the above runs without errors, you have installed things correctly.

#### Running the code on the Jetson Nano for detection

To run the detection, use the commands:

```bash
python yolo_object_detection.py -y model
```

This should pull up a screen with the live feed from the camera.

#### OpenCV compile CMake

```shell script
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D WITH_CUDA=ON \
	-D CUDA_ARCH_PTX="" \
	-D CUDA_ARCH_BIN="5.3,6.2,7.2" \
	-D WITH_CUBLAS=ON \
	-D WITH_LIBV4L=ON \
	-D BUILD_opencv_python3=ON \
	-D BUILD_opencv_python2=OFF \
	-D BUILD_opencv_java=OFF \
	-D WITH_GSTREAMER=ON \
	-D WITH_GTK=ON \
	-D BUILD_TESTS=OFF \
	-D BUILD_PERF_TESTS=OFF \
	-D BUILD_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/home/`whoami`/opencv_contrib/modules ..
```
