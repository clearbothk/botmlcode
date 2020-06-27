import json

#from .Location import Location
#from .Confidence import Confidence
#from .Label import Label

from Location import Location
from Confidence import Confidence
from Label import Label


class Report:
    def __init__(self, label, confidence, location):
        self.label = Label(label)
        self.confidence = Confidence(confidence)
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



    #def get_label(self):
    #    return yolo_object_detection.LABELS

    #def get_confidence(self):
    #    return yolo_object_detection.confidence

    #def get_location(self):
    #    return test1.do_capture_relative_global_location(self)

#report = Report("metal", 98.5, "hi")
#report.print_report()
#report.create_report()
#report.print_report()
#report.write_report('report_folder/report.json')
