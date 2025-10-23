import time
import csv

class logFile_class():
	def __init__(self):
		with open('data.csv', 'w', newline='') as csvfile:
			self.writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
			self.writer.writerow([
				"timestamp",
				"local_psp",
				"local_qsp",
				"total_pac",
				"total_qac"
			])
	
	def write_data(self, obj):
		# Write to csv
		with open('data.csv', 'a', newline='') as csvfile:
			self.writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
			self.writer.writerow([
				str(round(time.time(), 2)),
				str(round(obj.local_P_sp, 3)),
				str(round(obj.local_Q_sp, 3)),
				str(round(obj.p_actual_hv, 3)),
				str(round(obj.q_actual_hv, 3))
			])
