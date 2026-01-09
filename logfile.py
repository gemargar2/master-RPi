import time
import csv

class logFile_class():
	def __init__(self):
		self.init_file()
	
	def init_file(self):
		with open('data.csv', 'w', newline='') as csvfile:
			self.writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
			self.writer.writerow([
				"timestamp",
				"p_ex_sp",
				"q_ex_sp",
				"v_ex_sp",
				"pf_ex_sp",
				"p_actual_hv",
				"q_actual_hv",
				"f_actual_hv",
				"v_actual_hv",
				"pf_actual_hv"
			])
	
	def write_data(self, obj, start_time):
		# Write to csv
		with open('data.csv', 'a', newline='') as csvfile:
			self.writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
			self.writer.writerow([
				str(round(time.time()-start_time, 3)),
				str(round(obj.p_ex_sp, 3)),
				str(round(obj.q_ex_sp, 3)),
				str(round(obj.v_ex_sp, 3)),
				str(round(obj.pf_ex_sp, 3)),
				str(round(obj.p_actual_hv, 3)),
				str(round(obj.q_actual_hv, 3)),
				str(round(obj.f_actual, 3)),
				str(round(obj.v_actual, 3)),
				str(round(obj.pf_actual, 3))
			])
