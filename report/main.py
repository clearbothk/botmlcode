import time

from .pixhawk import Pixhawk
from .report import Report
from .reports import Reports

report_path = 'report_folder/report.json'
reports_path = 'report_folder/reports.json'

count = 0
reports = Reports()
while True:
	if (count % 2) == 0:
		pixhawk = Pixhawk()
		location_pixhawk = pixhawk.do_capture_global_location()
		report = Report("litter", 97, str(location_pixhawk))
		report.create_report()
		report.print_report()
		report.write_report(report_path)
		reports.combine(reports_path)
		time.sleep(5)
	count += 1
