import json

from .Location import Location
from .Confidence import Confidence
from .Label import Label


class Report:
    def __init__(self, yolo, location):
        self.label = Label(yolo)
        self.confidence = Confidence(yolo)
        self.location = Location(location)
        self.report = {}

    def create_report(self):
        report = {
            "label": self.label.get_label(),
            "confidence": self.confidence.get_confidence(),
            "location": self.location.get_coordinate()
        }
        self.report = report

    def print_report(self):
        print(self.report)

    def write_report(self, path):
        with open(path, 'w') as file_stream:
            json.dump(self.report, file_stream, indent=4, sort_keys= True)

