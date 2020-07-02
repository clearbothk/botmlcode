import json

from report.clearbot_attributes import *

class Report:
    def __init__(self, yolo, pixhawk):
        self.label = Label.Label(yolo)
        self.confidence = Confidence.Confidence(yolo)
        self.firmware_version = Firmware_version.Firmware_version(pixhawk)
        self.vehicle_capabilities = Vehicle_capabilities.Vehicle_capabilities(pixhawk)
        self.location = Location.Location(pixhawk)
        self.attitude = Attitude.Attitude(pixhawk)
        self.velocity = Velocity.Velocity(pixhawk)
        self.gps = Gps.Gps(pixhawk)
        self.ground_speed = Ground_speed.Ground_speed(pixhawk)
        self.air_speed = Air_speed.Air_speed(pixhawk)
        self.gimbal_status = Gimbal_status.Gimbal_status(pixhawk)
        self.battery_status = Battery_status.Battery_status(pixhawk)
        self.ekf_ok = Ekf_ok.Ekf_ok(pixhawk)
        self.last_heartbeat = Last_heartbeat.Last_heartbeat(pixhawk)
        self.range_finder_distance = Range_finder_distance.Range_finder_distance(pixhawk)
        self.range_finder_voltage = Range_finder_voltage.Range_finder_voltage(pixhawk)
        self.heading = Heading.Heading(pixhawk)
        self.vehicle_is_armable = Vehicle_is_armable.Vehicle_is_armable(pixhawk)
        self.system_status = System_status.System_status(pixhawk)
        self.vehicle_mode_name = Vehicle_mode_name.Vehicle_mode_name(pixhawk)
        self.check_vehicle_armed = Check_vehicle_armed.Check_vehicle_armed(pixhawk)
        self.report = {}

    def create_report(self):
        report = {
            "label": self.label.get_label(),
            "confidence": self.confidence.get_confidence(),
            "firmware_version" : self.firmware_version.get_version(),
			"vehicle_capabilities" : self.vehicle_capabilities.get_capabilities(),
			"location" :self.location.get_coordinate(),
            "attitude" : self.attitude.get_attitude(),
            "velocity" : self.velocity.get_velocity(),
            "gps" : self.gps.get_gps(),
            "ground_speed" : self.ground_speed.get_speed(),
            "air_speed" : self.air_speed.get_air_speed(),
            "gimbal_status" : self.gimbal_status.get_status(),
            "battery_status" : self.battery_status.get_battery(),
            "EKF_OK" : self.ekf_ok.get_ekf(),
            "last_heartbeat" : self.last_heartbeat.get_last_heartbeat(),
            "range_finder_distance" : self.range_finder_distance.get_distance(),
            "range_finder_voltage" : self.range_finder_voltage.get_voltage(),
            "heading" : self.heading.get_heading(),
            "vehicle_is_armable" : self.vehicle_is_armable.get_armable(),
            "system_status" : self.system_status.get_system_status(),
            "vehicle_mode_name" : self.vehicle_mode_name.get_name(),
            "check_vehicle_armed" : self.check_vehicle_armed.get_check()
        }
        self.report = report

    def print_report(self):
        print(self.report)

    def write_report(self, path):
        with open(path, 'w') as file_stream:
            json.dump(self.report, file_stream, indent=4, sort_keys= True)

