import numpy as np
import cv2
import os
import functools, operator

import logging


class Detector:
	weights_file = None
	config_file = None
	names_file = None

	confidence_threshold = 0
	nms_threshold = 0
	LABELS = []

	net = None
	ln = None

	def __init__(self, model_path="model", use_gpu=False, confidence_thres=0.5, nms_thres=0.3,
	             weights_file="clearbot.weights", config_file="clearbot.cfg", names_file="clearbot.names"):

		self.confidence_threshold = confidence_thres
		self.nms_threshold = nms_thres

		self.weights_file = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, weights_file])
		self.config_file = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, config_file])
		self.names_file = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), model_path, names_file])
		logging.debug("Finished initialising model file paths")

		try:
			self.LABELS = open(self.names_file).read().strip().split("\n")
			logging.debug(f"Loaded labels from the names file: \n{self.LABELS}")
		except Exception as e:
			logging.error(e)

		try:
			logging.debug("Loading Darknet model")
			self.net = cv2.dnn.readNetFromDarknet(self.config_file, self.weights_file)
			logging.debug("Finished loading Darknet model")
		except Exception as e:
			logging.error(e)

		if use_gpu:
			logging.info("Will try to use GPU backend")
			self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		else:
			logging.info("Using CPU only")

		self.ln = self.net.getLayerNames()

		unconnected_layers = functools.reduce(operator.iconcat, self.net.getUnconnectedOutLayers(), [])
		logging.debug(f"Indexes of unconnected layers: {unconnected_layers}")
		self.ln = [self.ln[i - 1] for i in unconnected_layers]
		logging.debug(f"Output layers for YOLO are: {self.ln}")

	def detect(self, frame):
		"""
		Detect the objects in the frame
		:param frame: Frame that has been captured from the OpenCV video stream
		:return: dict object with the objects and the bounding boxes
		"""
		(H, W) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (608, 608), swapRB=True, crop=False)

		self.net.setInput(blob)
		layer_outputs = self.net.forward(self.ln)

		boxes = []
		confidences = []
		class_ids = []

		for output in layer_outputs:
			for detection in output:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]

				if confidence > self.confidence_threshold:
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					x = int(centerX - (width / 2))
					y = int(centerY - (width / 2))

					# Adding int(width) and int(height) is really important for some reason.
					# Removing it gives an error in NMSBoxes() call
					# Shall figure out soon and write a justification here.
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					class_ids.append(class_id)

		logging.debug((boxes, confidences, self.confidence_threshold, self.nms_threshold))
		indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
		logging.debug(f"Indexes: {indexes}")
		if len(indexes) > 0:
			indexes = indexes.flatten()
		return map(lambda idx: self.detected_to_result(boxes[idx], confidences[idx], class_ids[idx]), indexes)

	def detected_to_result(self, box, confidence, class_id):
		(x, y) = (box[0], box[1])
		(w, h) = (box[2], box[3])

		label = self.LABELS[class_id]

		return {
			"label": label,
			"confidence": confidence,
			"bbox": {
				"x": x,
				"y": y,
				"width": w,
				"height": h
			}
		}


if __name__ == "__main__":
	logging.getLogger().setLevel(logging.DEBUG)

	detector = Detector()
