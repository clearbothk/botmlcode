import argparse
import logging
import multiprocessing
from multiprocessing import Queue

import cv2
from imutils.video import FPS

from detector import detector as dt
from report import report, thingspeak
from pixhawk import pixhawk as px

reports_path = 'report/report_folder/reports.json'
q = Queue(maxsize=0)


def writeData():
	logging.info("Starting connection to Pixhawk")
	try:
		pixhawk = px.Pixhawk()
		logging.info("Connected to Pixhawk")
	except Exception as e:
		return -1

	while True:
		while True:
			if (q.empty == False):
				logging.debug("Message queue is empty")
				break

		yolo_data = q.get()

		# post to thingspeak.com
		visualize = thingspeak.ThingSpeak(yolo_data, pixhawk)
		visualize.send_to_thingspeak()

		# saved to reports.json
		get_report = report.Report(yolo_data, pixhawk)
		get_report.create_report()
		get_report.print_report()
		get_report.write_report(reports_path)


def main(params):
	print("Yolo is starting")

	logging.info("accessing video stream...")
	vs = cv2.VideoCapture(0)
	detector = dt.Detector("model", use_gpu=True, weights_file="clearbot-tiny.weights", config_file="clearbot-tiny.cfg", confidence_thres=0.1)
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
