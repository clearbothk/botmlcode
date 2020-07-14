class AirSpeed:
	def __init__(self, y):
		self.y = y[7]

	def get_air_speed(self):
		return self.y


class Altitude:
	def __init__(self, y):
		self.y = y[3]

	def get_altitude(self):
		return self.y


class BatteryStatus:
	def __init__(self, y):
		self.y = y[9]

	def get_battery_status(self):
		return self.y


class CheckVehicleArmed:
	def __init__(self, y):
		self.y =

	def get_armed_status(self):
		return self.y


class Confidence:
	def __init__(self, y):
		self.y = y["confidence"]

	def get_confidence(self):
		return self.y


class EkfOK:
	def __init__(self, y):
		self.y = y[10]

	def get_ekf_status(self):
		return self.y


class FirmwareVersion:
	def __init__(self, y):
		self.y = y[0]

	def __version__(self):
		return self.y


class GimbalStatus:
	def __init__(self, y):
		self.y = y[8]

	def get_gimbal_status(self):
		return self.y


class GPS:
	def __init__(self, y):
		self.y = y[5]

	def get_gps(self):
		return self.y


class GroundSpeed:
	def __init__(self, y):
		self.y = y[6]

	def get_ground_speed(self):
		return self.y


class Heading:
	def __init__(self, y):
		self.y = y[14]

	def get_heading(self):
		return self.y


class Label:
	def __init__(self, x):
		self.x = x["label"]

	def get_label(self):
		return self.x


class LastHeartbeat:
	def __init__(self, y):
		self.y = y[11]

	def get_last_heartbeat(self):
		return self.y


class Location:
	def __init__(self, z):
		self.z = z[2]

	def get_coordinates(self):
		return self.z


class RangeFinderDistance:
	def __init__(self, y):
		self.y = y[12]

	def get_distance(self):
		return self.y


class RangeFinderVoltage:
	def __init__(self, y):
		self.y = y[13]

	def get_voltage(self):
		return self.y


class SystemStatus:
	def __init__(self, y):
		self.y = y[16]

	def get_system_status(self):
		return self.y


class VehicleCapabilities:
	def __init__(self, y):
		self.y = y[1]

	def get_capabilities(self):
		return self.y


class VehicleArmable:
	def __init__(self, y):
		self.y = y[15]

	def get_armable(self):
		return self.y


class VehicleModeName:
	def __init__(self, y):
		self.y = y[17]

	def get_mode_name(self):
		return self.y


class Velocity:
	def __init__(self, y):
		self.y = y[4]

	def get_velocity(self):
		return self.y
