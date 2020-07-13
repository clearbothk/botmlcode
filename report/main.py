import time
import cv2
from detector import yolo

from .pixhawk import Pixhawk
from .report import Report
from .reports import Reports

report_path = 'report_folder/report.json'
reports_path = 'report_folder/reports.json'

print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)
detector = yolo.Detector("model", use_gpu=True, weights_file="clearbot.weights")

reports = Reports()
previous = 0

while True:
	(grabbed, frame) = vs.read()
	if not grabbed:
		break
	result = detector.detect(frame)
	current = len(result)
	if (current > 0 and current > previous):
		result_object = result[current - 1]
		pixhawk = Pixhawk()
		yolo_result = result_object
		pixhawk_location = str(pixhawk.do_capture_global_location())
		report = Report(yolo_result, pixhawk_location)
		report.create_report()
		report.print_report()
		report.write_report(report_path)
		reports.combine(reports_path)
		previous = current
		time.sleep(5)
