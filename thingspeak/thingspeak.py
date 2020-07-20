import os
import paho.mqtt.publish as publish
import re
import logging


class ThingSpeak:
	def __init__(self, pixhawk, mqtt_host="mqtt.thingspeak.com"):
		CHANNEL_ID = os.environ['CHANNEL_ID']
		API_KEY = os.environ['API_KEY']
		self.location = pixhawk.do_capture_global_location()
		self.battery_status = pixhawk.battery_status()
		self.system_status = pixhawk.system_status()
		self.mqtt_host = mqtt_host
		self.mqtt_port = 1883
		self.topic = f"channels/{CHANNEL_ID}/publish/{API_KEY}"
		self.payload = None

	def create_payload_string(self):
		return "&".join(map(lambda x: f"{x[0]}={x[1]}", self.payload.items()))

	def update_thingspeak_payload(self):
		location_string = self.location.get_coordinates()
		gps_location = re.findall(r"[-+]?\d*\.\d+|\d+", location_string)
		lat = gps_location[0]
		lon = gps_location[1]

		battery_status_data = str(self.battery_status.get_battery_status())
		system_status_data = str(self.system_status.get_system_status())

		self.payload = {
			"field1": lat,
			"field2": lon,
			"field3": str(0),
			"field4": system_status_data,
			"field5": battery_status_data,
			"field6": str("None")
		}

	def send_to_thingspeak(self):
		self.update_thingspeak_payload()
		payload_string = self.create_payload_string()
		print("[INFO] Data prepared to be uploaded")

		try:
			publish.single(self.topic, payload=payload_string, hostname=self.mqtt_host, port=self.mqtt_port, tls=None, transport="tcp")
			print("[INFO] Data sent successfully")
		except Exception as e:
			logging.error(e)
