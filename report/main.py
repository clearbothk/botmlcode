import time

from .pixhawk import Pixhawk
from .report import Report

count = 0
while True:
	if (count % 2) == 0:
		pixhawk = Pixhawk()
		location_pixhawk = pixhawk.do_capture_global_location()
		report = Report("litter", 97, str(location_pixhawk))
		report.create_report()
		report.print_report()
		report.write_report('report_folder/report.json')

		time.sleep(5)
	count += 1
