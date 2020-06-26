#import asyncio
import sys
import os
import time


sys.path.insert(0, "/botmlcode/")

#from yolo_object_detection import yolo_object_detection
from pixhawk import Pixhawk
from report import Report 

#yolo_object_detection.run()
#time.sleep(60)
count = 0
while True:
    if (count % 2)==0:
        pixhawk = Pixhawk()
        location_pixhawk = pixhawk.do_capture_global_location()
        #label_yolo = yolo_object_detection.LABEL() 
        #confidence_yolo = yolo_object_detection.confidence()
        report = Report("litter", 97, str(location_pixhawk))
        report.create_report()
        report.print_report()
        report.write_report('report_folder/report.json')
        
        time.sleep(5)
    count += 1
    
    
    









