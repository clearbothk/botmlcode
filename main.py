import time
import cv2
from detector import yolo
from report import report
from report import reports
from report import pixhawk

report_path = 'report/report_folder/report.json'
reports_path = 'report/report_folder/reports.json'

print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(1)
detector = yolo.Detector("model", use_gpu=True, weights_file="clearbot_26_06_20.weights")

reports = reports.Reports()
previous = 0

while True:
	(grabbed, frame) = vs.read()
	if not grabbed:
		break
	result = detector.detect(frame)
	current = len(result)
	if (current > 0 and current > previous):
		result_object = result[current - 1]
		pixhawk = pixhawk.Pixhawk()
		pixhawk_data = pixhawk.get_data()
		yolo_result = result_object
		report = report.Report(yolo_result, pixhawk_data)
		report.create_report()
		report.print_report()
		report.write_report(report_path)
		reports.combine(reports_path)
		previous = current
		time.sleep(5)
# from detector import yolo
# import cv2

# """
# Sample code importing the detector module
# """
# print("[INFO] accessing video stream...")
# vs = cv2.VideoCapture(0)
# detector = yolo.Detector("model", use_gpu=True, weights_file="clearbot_26_06_20.weights")
# while True:
# 	(grabbed, frame) = vs.read()
# 	if not grabbed:
# 		break
# 	result = detector.detect(frame)
# 	print(result)
