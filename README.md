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

### Misc instructions if you have not compiled OpenCV yet

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


# Setup on the Jetson Nano board for Pixhawk


we are using [DroneKit-Python API](https://dronekit-python.readthedocs.io/en/latest/about/overview.html) as an Onboard app between Jetson Nano and Pixhawk. 

Make sure your linux userid has the permission to use your tty port device

connection port = `dev/ttyTHS1`

Assume our userid is `user`
```bash
sudo usermod -a -G dialout user
```
let's try running `testing.py` to get a brief introduction with `Dronekit` ( in `botmlcode/` directory )

```bash
python testing.py
```
we are aware that we need to wait for around `10 seconds` or more to get the above's print statement be executed. At first, we though this was an issue( listed below )
* Note ( 14th July, 2020): Optimise Pixhawk integration to the Jetson #5 [Track the issue here](https://github.com/clearbothk/botmlcode/issues/5)

In `pixhawk.py` script, below is the line code to establish Dronekit connectivity to the connected device. it is recommended to set [wait_ready=True](https://dronekit-python.readthedocs.io/en/latest/guide/connecting_vehicle.html) to waits until some vehicle parameters and attributes are populated so that it is initialized successfully.

```python
def __init__(self, connection_port="/dev/ttyTHS1", baud=57600):
		try:
			self.vehicle = connect(connection_port, wait_ready=True, baud=baud)
			self.vehicle.mode = VehicleMode("MANUAL")
		except serialutil.SerialException as e:
			logging.error(e)
````
Thus we need to first initialize the `dronekit.connect()` and make it as a constructor  rather than repeatedly run the scripts so that we do not need to re run the script for everytime the [Dronekit attributes functions](https://dronekit-python.readthedocs.io/en/latest/guide/vehicle_state_and_parameters.html)
 get called.

 # Angle measurement 
 
### Requirements

- OpenCV (latest version from the repo: see setup instructions for details)
- Python 3.6 or above
- Numpy (latest version)

Make sure the clearbot camera has already been calibrated. If you are using a different camera or you want to calibrate the camera again, [click here](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html) for reference. Make sure to calculate the distance between the camera to the calibration checkboard and calculate the half of the value of horizontal length of the calibration checkboard. You can find the `Check_board.pdf` image inside `imgsrc/` directory. 


![alt text](imgsrc/pinhole_camera_model.png?raw=true)

Below is the `get_angle()` function. It is located in `detector.py`
```python
	def get_angle(self, x_axis):
		real_distance = 0
		angle = 0
		if (x_axis < 316):
			x_axis = 316 - x_axis
			real_distance = (14.5 * x_axis)/316
			angle = np.degrees(np.math.atan2(real_distance, 45))
		
		elif (x_axis > 316):
			x_axis = x_axis - 316
			real_distance = (14.5 * x_axis)/316
			angle = np.degrees(np.math.atan2(real_distance, 45))

		else:
			angle = 0
		return angle
```
- Let the distance between the camera to the calibration checkboard as X 

- Let the half of the value its horizontal length of the calibration checkboard as Y

In this current configuration, X = 45 and Y = 14.5. By using the inverse tangent function we can get the maximum angle that the camera gets. We can use [NumPy](https://numpy.org/doc/stable/reference/generated/numpy.degrees.html) library by using `np.degrees(np.math.atan2(real_distance, 45))`. real_distance depends on where the object at.

 If the object's x_axis is located in the 2nd and 3rd quadrant, then the real_distance is:

 `(Y * ((horizantal pixel length / 2) - x_axis)/ (horizantal pixel length / 2)`. 


On the other hand, if the if the object's x_axis is located in the 1st and 4th quadrant, then the real_distance is:
`(Y * (x_axis - (horizantal pixel length / 2)))/ (horizantal pixel length / 2)`.


