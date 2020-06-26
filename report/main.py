import asyncio
import sys
import os
import time


sys.path.insert(1, "/botmlcode/")

from yolo_object_detection import yolo_object_detection
from pixhawk import pixhawk
from report import Report 

yolo_object_detection.run()

while True:
    if (yolo_object_detection.detected):
        pixhawk.run()
        time.sleep(10)
        location_pixhawk = pixhawk.vehicle.do_capture_global_location()
        label_yolo = yolo_object_detection.LABEL 
        confidence_yolo = yolo_object_detection.confidence
        report = Report(label_yolo, confidence_yolo, location_pixhawk)
        report.create_report()
        report.print_report()
        report.write_report('report_folder/report.json')

    else:
        pass
    
    









