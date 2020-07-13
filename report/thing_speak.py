import paho.mqtt.publish as publish
from report.clearbot_attributes import *
import time
import re
import config

topic = "channels/"+ config.CHANNEL_ID +"/publish/"+ config.API_KEY
mqttHost = "mqtt.thingspeak.com"
tTransport = "tcp"
tPort = 1883
tTLS = None


class Thing_speak:

    def __init__(self,yolo, pixhawk):
        self.label = Label.Label(yolo)
        self.confidence = Confidence.Confidence(yolo)
        self.location = Location.Location(pixhawk)
        self.battery_status = Battery_status.Battery_status(pixhawk)
        self.system_status = System_status.System_status(pixhawk)
        
    def show_thingspeak(self):
        #get gps_location from string variable and stored it in a list
        location_string = self.location.get_coordinate()
        gps_location = re.findall(r"[-+]?\d*\.\d+|\d+", location_string)
        
        label_data = str(self.label.get_label())
        confidence_data = str(self.confidence.get_confidence()*100)
        lat = gps_location[0]
        lon = gps_location[1]
        battery_status_data = str(self.battery_status.get_battery())
        system_status_data = str(self.system_status.get_system_status())

        #payload
        tPayload = "field1=" + lat + "&field2=" + lon + "&field3=" + confidence_data + "&field4=" + system_status_data + "&field5=" + battery_status_data + "&field6=" + label_data

        print("[INFO] Data prepared to be uploaded")
    
        try:
            #publish the data
            publish.single(topic, payload = tPayload, hostname = mqttHost, port = tPort, tls = tTLS, transport = tTransport)
            print("[INFO] Data sent successfully")
        except:
            print("[INFO] Failure in sending data")