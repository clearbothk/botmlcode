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

	model_file = ""
	cfg_file = ""
	if args.model == "tiny":
		model_file = "clearbot-tiny.weights"
		cfg_file = "clearbot-tiny.cfg"
	elif args.model == "full":
		model_file = "clearbot.weights"
		cfg_file = "clearbot.cfg"
	detector = dt.Detector("model", use_gpu=True, weights_file=model_file, config_file=cfg_file,
	                       confidence_thres=0.5)
	fps = FPS().start()

	while True:
		(grabbed, frame) = vs.read()
		if not grabbed:
			break
		result = detector.detect(frame)

		# If there is more than One object, find the nearest one and get the angle
		"""
		Detect the objects in the frame
		TO DO List:
		1. Find the coordinate of each object to the center point of the camera
		2. Find the nearest one using Euclidean distance
		"""
		angle = detector.get_angle(frame)
		#print(angle)
		for box in result:
			bbox = box["bbox"]
			label = box["label"]
			x = bbox["x"]
			y = bbox["y"]
			w = bbox["width"]
			h = bbox["height"]
			cv2.rectangle(img=frame,
			              pt1=(x, y),
			              pt2=(x + w, y + h),
			              color=(36, 255, 12),
			              thickness=2)
			cv2.putText(img=frame,
			            text=label,
			            org=(x, y - 10),
			            fontFace=cv2.FONT_HERSHEY_COMPLEX,
			            fontScale=0.7,
			            color=(36, 255, 12),
			            thickness=2)

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
	parser.add_argument('-m', '--model', type=str, default="tiny", help="Either tiny or full")
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
