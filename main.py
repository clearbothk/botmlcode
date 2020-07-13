import time
import argparse
import logging
import multiprocessing
from serial import serialutil
from imutils.video import FPS
import cv2
from queue import Queue

from detector import detector as dt
from report import report
from report import reports
from report import pixhawk
from report import thingspeak

report_path = 'report/report_folder/report.json'
reports_path = 'report/report_folder/reports.json'
q = Queue(maxsize=0)


def writeData():
	while True:
		while True:
			if (q.empty == False):
				logging.debug("Message queue is empty")
				break

		try:
			yolo_data = q.get()
			pixhawk_init = pixhawk.Pixhawk()
			pixhawk_data = pixhawk_init.get_data()
			logging.debug(pixhawk_data)

			# post to thingspeak.com
			logging.debug(f"Sending data to ThingSpeak:\n{yolo_data}\n{pixhawk_data}")
			visualize = thingspeak.ThingSpeak(yolo_data, pixhawk_data)
			visualize.show_thingspeak()

			# saved to reports.json
			get_report = report.Report(yolo_data, pixhawk_data)
			get_report.create_report()
			get_report.print_report()
			get_report.write_report(report_path)
			reports.combine(reports_path)
			return 0

		except serialutil.SerialException as e:
			# @utkarsh867: 9th July, 2020
			# I added this exception handler so that the code does not crash when it does not find a serial connection
			# to the Pixhawk
			logging.error(e)
			return -1


def main(params):
	print("Yolo is starting")

	logging.info("accessing video stream...")
	vs = cv2.VideoCapture(0)
	detector = dt.Detector("model", use_gpu=True)
	fps = FPS().start()

	while True:
		(grabbed, frame) = vs.read()
		if not grabbed:
			break
		result = detector.detect(frame)
		for box in result:
			bbox = box["bbox"]
			x = bbox["x"]
			y = bbox["y"]
			w = bbox["width"]
			h = bbox["height"]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

		logging.debug(result)

		for r in result:
			q.put(r)
		# This loop is iterating over all YOLO results
		# TODO: Optimise this section so that each frame is sent only once.

		if params.video_out:
			cv2.imshow("Clearbot", frame)
			# If this is not there, frame will not actually show: I did not dig into the explanation
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		fps.update()

	fps.stop()
	logging.info("approx. FPS: {:.2f}".format(fps.fps()))
	vs.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Clearbot AI and PController")
	parser.add_argument('-v', '--video_out', type=bool, default=False, help="Show the camera video output")
	parser.add_argument('--debug', type=bool, default=False, help="Switch to debug mode")
	args = parser.parse_args()

	# Added the logging package instead of printing data randomly
	if args.debug:
		logging.getLogger('root').setLevel(logging.DEBUG)
	else:
		logging.getLogger('root').setLevel(logging.INFO)

	# Set multiprocessing
	p1 = multiprocessing.Process(target=main, args=(args,))
	p2 = multiprocessing.Process(target=writeData)

	# Start Multiprocessing
	p1.start()
	p2.start()

	p1.join()
	p2.join()
