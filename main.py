import time
import cv2

from detector import yolo
from report import report
from report import reports
from report import pixhawk
from report import thing_speak

report_path = 'report/report_folder/report.json'
reports_path = 'report/report_folder/reports.json'

print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)
detector = yolo.Detector("model", use_gpu=True, weights_file="clearbot_26_06_20.weights")

reports = reports.Reports()
previous = 0

while True:
	(grabbed, frame) = vs.read()
	if not grabbed:
		break
	result = detector.detect(frame)
	current = len(result)
	print(result)
	if (current > 0):
		result_object = result[current - 1]
		pixhawk_init = pixhawk.Pixhawk()
		pixhawk_data = pixhawk_init.get_data()
		print(pixhawk_data)
		yolo_result = result_object

		#post to thingspeak.com
		visualize = thing_speak.Thing_speak(yolo_result, pixhawk_data)
		visualize.show_thingspeak()

		#saved to reports.json
		get_report = report.Report(yolo_result, pixhawk_data)
		get_report.create_report()
		get_report.print_report()
		get_report.write_report(report_path)
		reports.combine(reports_path)