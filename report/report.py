import json

from report.attributes import *


class Report:
	def __init__(self, yolo, pixhawk):
		self.label = Label(yolo)
		self.confidence = Confidence(yolo)
		self.firmware_version = FirmwareVersion(pixhawk)
		self.vehicle_capabilities = VehicleCapabilities(pixhawk)
		self.location = Location(pixhawk)
		self.attitude = Altitude(pixhawk)
		self.velocity = Velocity(pixhawk)
		self.gps = GPS(pixhawk)
		self.ground_speed = GroundSpeed(pixhawk)
		self.air_speed = AirSpeed(pixhawk)
		self.gimbal_status = GimbalStatus(pixhawk)
		self.battery_status = BatteryStatus(pixhawk)
		self.ekf_ok = EkfOK(pixhawk)
		self.last_heartbeat = LastHeartbeat(pixhawk)
		self.range_finder_distance = RangeFinderDistance(pixhawk)
		self.range_finder_voltage = RangeFinderVoltage(pixhawk)
		self.heading = Heading(pixhawk)
		self.vehicle_is_armable = VehicleArmable(pixhawk)
		self.system_status = SystemStatus(pixhawk)
		self.vehicle_mode_name = VehicleModeName(pixhawk)
		self.check_vehicle_armed = CheckVehicleArmed(pixhawk)
		self.report = {}

	def create_report(self):
		report = {
			"label": self.label.get_label(),
			"confidence": self.confidence.get_confidence(),
			"firmware_version": self.firmware_version.__version__(),
			"vehicle_capabilities": self.vehicle_capabilities.get_capabilities(),
			"location": self.location.get_coordinates(),
			"attitude": self.attitude.get_altitude(),
			"velocity": self.velocity.get_velocity(),
			"gps": self.gps.get_gps(),
			"ground_speed": self.ground_speed.get_ground_speed(),
			"air_speed": self.air_speed.get_air_speed(),
			"gimbal_status": self.gimbal_status.get_gimbal_status(),
			"battery_status": self.battery_status.get_battery_status(),
			"EKF_OK": self.ekf_ok.get_ekf_status(),
			"last_heartbeat": self.last_heartbeat.get_last_heartbeat(),
			"range_finder_distance": self.range_finder_distance.get_distance(),
			"range_finder_voltage": self.range_finder_voltage.get_voltage(),
			"heading": self.heading.get_heading(),
			"vehicle_is_armable": self.vehicle_is_armable.get_armable(),
			"system_status": self.system_status.get_system_status(),
			"vehicle_mode_name": self.vehicle_mode_name.get_mode_name(),
			"check_vehicle_armed": self.check_vehicle_armed.get_armed_status()
		}
		self.report = report

	def print_report(self):
		print(self.report)

	def write_report(self, path):
		with open(path, 'w') as file_stream:
			json.dump(self.report, file_stream, indent=4, sort_keys=True)
