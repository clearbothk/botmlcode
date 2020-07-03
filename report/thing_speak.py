import paho.mqtt.publish as publish
from report.clearbot_attributes import *
import time

channelID = "1092630"
apiKey = "FGN0JQQLW5D88TJ1"

topic = "channels/"+ channelID +"/publish/"+ apiKey
mqttHost = "mqtt.thingspeak.com"
tTransport = "tcp"
tPort = 1883
tTLS = None


class Thing_speak:

    def __init__(yolo_result, pixhawk_data):
        self.label = Label.Label(yolo)
        self.confidence = Confidence.Confidence(yolo)
        self.location = Location.Location(pixhawk)
        self.battery_status = Battery_status.Battery_status(pixhawk)
        self.system_status = System_status.System_status(pixhawk)
        
    def show_thingspeak(self):
        #get gps_location from string variable and stored it in a list
        gps_location=[]
        location_string = self.location.get_coordinate()
        location_list = location_string.split()
        for i in location_list:
            try:
                result = float(i)
                gps_location.append(result)
            except:
                continue

        #payload
        tPayload = "field1=" + gps_location + "&field2=" + str(self.label.get_label()) + "&field3=" + str(self.confidence.get_confidence()) + "&field4=" + str(self.system_status.get_system_status()) + "&field5=" + str(self.battery_status.get_battery())

        print("[INFO] Data prepared to be uploaded")
    
        try:
            #publish the data
            publish.single(topic, payload = tPayload, hostname = mqttHost, port = tPort, tls = tTLS, transport = tTransport)
            print("[INFO] Data send for two fields: ")
        except:
            print("[INFO] Failure in sending data")