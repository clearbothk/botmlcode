import os
import paho.mqtt.publish as publish
import re
import logging

# topic = "channels/"+ config.CHANNEL_ID +"/publish/"+ config.API_KEY
topic = "channels/publish"
mqttHost = "mqtt.thingspeak.com"
tTransport = "tcp"
tPort = 1883
tTLS = None


class ThingSpeak:
	def __init__(self, yolo, pixhawk):
		self.label = yolo["label"]
		self.confidence = yolo["confidence"]
		self.location = pixhawk.do_capture_global_location()
		self.battery_status = pixhawk.battery_status()
		self.system_status = pixhawk.system_status()

	def create_payload_string(self, payload):
		return "&".join(map(lambda x: f"{x[0]}={x[1]}", payload.items()))

	def send_to_thingspeak(self):
		# get gps_location from string variable and stored it in a list
		location_string = self.location.get_coordinates()
		gps_location = re.findall(r"[-+]?\d*\.\d+|\d+", location_string)

		label_data = str(self.label.get_label())
		confidence_data = str(self.confidence.get_confidence() * 100)
		lat = gps_location[0]
		lon = gps_location[1]
		battery_status_data = str(self.battery_status.get_battery_status())
		system_status_data = str(self.system_status.get_system_status())

		# payload
		payload = {
			"field1": lat,
			"field2": lon,
			"field3": confidence_data,
			"field4": system_status_data,
			"field5": battery_status_data,
			"field6": label_data
		}

		payload_string = self.create_payload_string(payload)

		print("[INFO] Data prepared to be uploaded")

		try:
			# publish the data
			publish.single(topic, payload=payload_string, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
			print("[INFO] Data sent successfully")
		except Exception as e:
			logging.error(e)
