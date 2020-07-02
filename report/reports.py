from pathlib import Path
import json

data_folder = Path("report/report_folder/")
file_to_open = data_folder / "report.json"

class Reports:

    def __init__(self):
        self.json_object= {}
        self.reports_array= []

    def combine(self, path):
        with open(file_to_open, 'r') as open_file:
            self.json_object= json.load(open_file)
        
        with open(path, 'r') as file_stream:
            reports_json = json.load(file_stream)

        if(reports_json.get("Clearbot") != None):
            self.reports_array = reports_json["Clearbot"]
            self.reports_array.append(self.json_object)
        else:
            self.reports_array = [self.json_object]

        with open(path, 'w') as write_file:
            json.dump({ 'Clearbot': self.reports_array }, write_file, indent=4, sort_keys=True)



    