import asyncio
import sys
import os
import time


sys.path.insert(1, "/botmlcode/")


from yolo_object_detection import yolo_object_detection
from dronekit import dronekit

def run():
    os.system('python /botmlcode/yolo_object_detection.py')
    time.sleep(60)

    









