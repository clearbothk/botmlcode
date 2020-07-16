import argparse
import logging
import multiprocessing
import cv2
from imutils.video import FPS
from detector import detector as dt
from report import report
from thingspeak import thingspeak
from pixhawk import pixhawk as px


def pixhawk_controller():
	logging.info("Starting connection to Pixhawk")
	try:
		pixhawk = px.Pixhawk()
		visualize = thingspeak.ThingSpeak(pixhawk)
		logging.info("Connected to Pixhawk")
	except Exception as e:
		logging.error(e)
		return -1

	while True:
		system_report = report.SystemReport(pixhawk)
		system_report.create_report()
		system_report.print_report()
		system_report.write_report()

		visualize.send_to_thingspeak()


def object_detection(params):
	logging.info("Accessing video stream...")
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

		if params.video_out:
			cv2.imshow("Clearbot", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		fps.update()

	fps.stop()
	logging.debug("approx. FPS: {:.2f}".format(fps.fps()))
	vs.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Clearbot AI and PController")
	parser.add_argument('-v', '--video_out', type=bool, default=False, help="Show the camera video output")
	parser.add_argument('--debug', type=bool, default=False, help="Switch to debug mode")
	args = parser.parse_args()

	if args.debug:
		logging.getLogger('root').setLevel(logging.DEBUG)
	else:
		logging.getLogger('root').setLevel(logging.INFO)

	p1 = multiprocessing.Process(target=object_detection, args=(args,))
	p2 = multiprocessing.Process(target=pixhawk_controller)

	p1.start()
	p2.start()

	p1.join()
	p2.join()
