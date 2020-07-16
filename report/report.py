import json


class Report:
	def __init__(self, yolo, pixhawk):
		self.label = yolo["label"]
		self.confidence = yolo["confidence"]
		self.firmware_version = pixhawk.firmware_version()
		self.vehicle_capabilities = pixhawk.vehicle_capabilities()
		self.location = pixhawk.do_capture_global_location()
		self.attitude = pixhawk.do_capture_attitude()
		self.velocity = pixhawk.do_capture_velocity()
		self.gps = pixhawk.do_capture_gps()
		self.ground_speed = pixhawk.do_capture_ground_speed()
		self.air_speed = pixhawk.do_capture_air_speed()
		self.gimbal_status = pixhawk.gimbal_status()
		self.battery_status = pixhawk.battery_status()
		self.ekf_ok = pixhawk.EKF_OK()
		self.last_heartbeat = pixhawk.last_heartbeat()
		self.range_finder_distance = pixhawk.range_finder_distance()
		self.range_finder_voltage = pixhawk.range_finder_voltage()
		self.heading = pixhawk.heading()
		self.vehicle_is_armable = pixhawk.vehicle_is_armable()
		self.system_status = pixhawk.system_status()
		self.vehicle_mode_name = pixhawk.vehicle_mode_name()
		self.check_vehicle_armed = pixhawk.check_vehicle_armed()
		self.report = {}

	def create_report(self):
		self.report = {
			"label": self.label,
			"confidence": self.confidence,
			"firmware_version": self.firmware_version,
			"vehicle_capabilities": self.vehicle_capabilities,
			"location": self.location,
			"attitude": self.attitude,
			"velocity": self.velocity,
			"gps": self.gps,
			"ground_speed": self.ground_speed,
			"air_speed": self.air_speed,
			"gimbal_status": self.gimbal_status,
			"battery_status": self.battery_status,
			"EKF_OK": self.ekf_ok,
			"last_heartbeat": self.last_heartbeat,
			"range_finder_distance": self.range_finder_distance,
			"range_finder_voltage": self.range_finder_voltage,
			"heading": self.heading,
			"vehicle_is_armable": self.vehicle_is_armable,
			"system_status": self.system_status,
			"vehicle_mode_name": self.vehicle_mode_name,
			"check_vehicle_armed": self.check_vehicle_armed
		}

	def print_report(self):
		print(self.report)

	def read_report_json(self, path):
		with open(path, 'r') as f:
			data = json.load(f)
			return data

	def write_report(self, path):
		currentJSONDump = self.read_report_json(path)
		currentJSONDump.append(self.report)
		with open(path, 'w') as file_stream:
			json.dump(currentJSONDump, file_stream, indent=2, sort_keys=True)
