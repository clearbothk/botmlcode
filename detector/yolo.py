import numpy as np
import cv2
import os


class Detector:
	net = None
	confidence_threshold = 0
	nms_threshold = 0
	LABELS = None
	ln = None

	def __init__(self, model_path, use_gpu=False, confidence_thres=0.5, nms_thres=0.3, weights_file="clearbot_26_06_20.weights",
	             config_file="clearbot.cfg", names_file="clearbot.names"):
		"""
		Initialise a instance for YOLOv4 object detection.
		:param model_path: The path of the model relative to the python script
		:param use_gpu: Whether to use GPU CUDA or not.
		:param confidence_thres: The confidence threshold of the results (0 to 1).
		:param nms_thres: The NMS threshold of the results
		"""
		self.confidence_threshold = confidence_thres
		self.nms_threshold = nms_thres

		labels_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, names_file])
		self.LABELS = open(labels_path).read().strip().split("\n")

		weights_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, weights_file])
		config_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, config_file])
		print("[INFO] loading YOLO from disk...")
		self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

		if use_gpu:
			# set CUDA as the preferable backend and target
			print("[INFO] setting preferable backend and target to CUDA...")
			self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

		# determine only the *output* layer names that we need from YOLO
		self.ln = self.net.getLayerNames()
		self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

	def detect(self, frame):
		"""
		Detect the objects in the frame
		:param frame: Frame that has been captured from the OpenCV video stream
		:return: dict object with the objects and the bounding boxes
		"""

		# construct a blob from the input frame and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes
		# and associated probabilities
		(H, W) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(
			frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
		)
		self.net.setInput(blob)
		layer_outputs = self.net.forward(self.ln)

		boxes = []
		confidences = []
		class_ids = []

		for output in layer_outputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability)
				# of the current object detection
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.confidence_threshold:
					# scale the bounding box coordinates back relative to
					# the size of the image, keeping in mind that YOLO
					# actually returns the center (x, y)-coordinates of
					# the bounding box followed by the boxes' width and
					# height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top
					# and and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates,
					# confidences, and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					class_ids.append(class_id)

		# Gives the indexes of the boxes that we should use
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
		result = []

		# Extract the results from the detector
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
				class_id = class_ids[i]
				label = self.LABELS[class_id]
				confidence = confidences[i]
				result.append({
					"label": label,
					"confidence": confidence,
					"bbox": {
						"x": x,
						"y": y,
						"width": w,
						"height": h
					}
				})
		return result

# Sample code for using object detection
# print("[INFO] accessing video stream...")
# vs = cv2.VideoCapture(0)
# detector = Detector("model", use_gpu=True, weights_file="clearbot_26_06_20.weights")
# while True:
# 	(grabbed, frame) = vs.read()
# 	if not grabbed:
# 		break
# 	result = detector.detect(frame)
