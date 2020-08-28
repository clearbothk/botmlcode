# Documentation for setting up Jetson Nano
 ## Some basic guidelines
 - The commands below are quite specific. This means that the following things should be avoided

- **DO NOT** use **sudo** where not specified. If you are facing issues, re-evaluate your actions and its consequences. Make sure that you followed the steps.
- Make sure that you are using virtual environment where specified. Virtual environment, while it seems insignificant, is actually mandatory.

## 1. Clone the Botmlcode repo
```bash
git clone https://github.com/clearbothk/botmlcode.git
```
## 2. Install pip

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

After installation is finished, restart the Jetson Nano

## 3. Setup and activate the virtualenv

```bash
pip install virtualenv --user
cd ~/botmlcode
virtualenv .venv -p python3
```

Then, to activate the virtual environment, run:

```bash
cd ~/botmlcode
source .venv/bin/activate
```

## 4. Install numpy in virtualenv

```bash
pip install numpy
```

## 5. Clone the opencv and opencv-contrib repo in the home directory

```bash
cd ~
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

If the clone for opencv is slow, download the zip from GitHub. Extract and rename the folder to opencv

Useful links when doing that:

[https://itsfoss.com/mount-exfat/](https://itsfoss.com/mount-exfat/)

## 6. Build OpenCV

Install un-installed dependencies in Jetson Nano

```bash
sudo apt install python3-dev
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
```

```bash
cd ~/opencv
mkdir build
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

Now make OpenCV

```bash
# Use nproc to check no. of threads
nproc
# 4

make -j4
```

Once its built, go to the botmlcode folder and symlink the built OpenCV python:

```bash
cd .venv/lib/python3.6/site-packages
ln -s /home/clearbot/opencv/build/lib/python3/cv2.cpython-36m-aarch64-linux-gnu.so cv2.so
```

## 7. Getting the code prepared to run

Pull the model data using Git LFS. In the botmlcode repo, run:

```bash
git lfs pull
```

### Note: In case Git LFS is not installed:

Install Git LFS using:

```bash
sudo apt install git-lfs
git lfs install
```

Next, install DroneKit and MAVProxy:

References:

[https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html](https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html)

[https://brisbaneroboticsclub.id.au/connect-nvidia-nano-to-pixhawk/](https://brisbaneroboticsclub.id.au/connect-nvidia-nano-to-pixhawk/)

```bash
sudo apt install libxml2-dev libxslt1-dev
# Make sure that you have activated the .venv using: $ source .venv/bin/activate
pip install matplotlib lxml
pip install future pymavlink mavproxy
pip install dronekit dronekit-sitl
```

Install MQTT for ThingSpeak

```bash
pip install paho-mqtt
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

 # Main functionality

 The intuition behind Botmlcode is to integrate Clearbot AI vision, Clearbot autonomous system, and the reporting system.

 To run the botmlcode `main.py`, we have the flexibility to conifgure which AI model that we want to use by using `-m tiny or full`. moreover, we also have the option to generate the video out and actiavte the debug fucntion by indcating `-v True` and `--debug True` respectively.

 There are two main function inside Botmlcode: 
 - The first one is the Object detection feature where the functions returns a list of all objects that are detected and also the Angle between the object and the optical axis of the camera using `get_angle()` function explained on the `Angle Measurement section` below. 

 - The second function is the `pixhawk_controller()`, make sure Jetson Nano is already configured with Pixhawk. the function return a Json log file where it consists of various data and status about the ClearBot such as the GPS location, velocity, battery status, and etc. 
 
 Both functions runs using [Multiprocessing module](https://docs.python.org/3/library/multiprocessing.html) to prevent dependency as it will risk the performances of the AI model.  



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


