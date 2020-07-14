from dronekit import connect, VehicleMode, LocationGlobalRelative


class Pixhawk:
	vehicle = None

	def __init__(self, connection_port="/dev/ttyTHS1", baud=57600):
		self.vehicle = connect(connection_port, wait_ready=True, baud=baud)
		self.vehicle.mode = VehicleMode("MANUAL")
		self.result = []

	def firmware_version(self):
		return self.vehicle.version

	def vehicle_capabilities(self):
		return self.vehicle.capabilities.ftp

	def do_capture_global_location(self):
		return self.vehicle.location.global_frame

	def do_capture_relative_global_location(self):
		return self.vehicle.location.global_relative_frame

	def do_capture_altitude(self):
		return self.vehicle.altitude

	def do_capture_velocity(self):
		return self.vehicle.velocity

	def do_capture_gps(self):
		return self.vehicle.gps_0

	def do_capture_ground_speed(self):
		return self.vehicle.groundspeed

	def do_capture_air_speed(self):
		return self.vehicle.airspeed

	def gimbal_status(self):
		return self.vehicle.gimbal

	def battery_status(self):
		return self.vehicle.battery

	def EKF_OK(self):
		return self.vehicle.ekf_ok

	def last_heartbeat(self):
		return self.vehicle.last_heartbeat

	def range_finder(self):
		return self.vehicle.rangefinder

	def range_finder_distance(self):
		return self.vehicle.rangefinder.distance

	def range_finder_voltage(self):
		return self.vehicle.rangefinder.voltage

	def heading(self):
		return self.vehicle.heading

	def vehicle_is_armable(self):
		return self.vehicle.is_armable

	def system_status(self):
		return self.vehicle.system_status.state

	def vehicle_mode_name(self):
		return self.vehicle.mode.name

	def check_vehicle_armed(self):
		return self.vehicle.armed

	def debug(self):
		print('Autopilot Firmware version: %s' % self.vehicle.version)
		print('Autopilot capabilities (supports ftp): %s' % self.vehicle.capabilities.ftp)
		print('Global Location: %s' % self.vehicle.location.global_frame)
		print('Global Location (relative altitude): %s' % self.vehicle.location.global_relative_frame)
		print('Local Location: %s' % self.vehicle.location.local_frame)
		print('Attitude: %s' % self.vehicle.attitude)
		print('Velocity: %s' % self.vehicle.velocity)
		print('GPS: %s' % self.vehicle.gps_0)
		print('Groundspeed: %s' % self.vehicle.groundspeed)
		print('Airspeed: %s' % self.vehicle.airspeed)
		print('Gimbal status: %s' % self.vehicle.gimbal)
		print('Battery: %s' % self.vehicle.battery)
		print('EKF OK?: %s' % self.vehicle.ekf_ok)
		print('Last Heartbeat: %s' % self.vehicle.last_heartbeat)
		print('Rangefinder: %s' % self.vehicle.rangefinder)
		print('Rangefinder distance: %s' % self.vehicle.rangefinder.distance)
		print('Rangefinder voltage: %s' % self.vehicle.rangefinder.voltage)
		print('Heading: %s' % self.vehicle.heading)
		print('Is Armable?: %s' % self.vehicle.is_armable)
		print('System status: %s' % self.vehicle.system_status.state)
		print('Mode: %s' % self.vehicle.mode.name)
		print('Armed: %s' % self.vehicle.armed)
