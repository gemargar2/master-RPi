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
				"p_in_sp",
				"q_in_sp",
				"q_in_up",
				"q_in_dn",
				"q_in_63",
				"q_in_90",
				"p_actual_hv",
				"q_actual_hv"
			])
	
	def write_data(self, obj, start_time):
		# Write to csv
		with open('data.csv', 'a', newline='') as csvfile:
			self.writer = csv.writer(csvfile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
			self.writer.writerow([
				str(round(time.time()-start_time, 3)),
				str(round(obj.p_in_sp, 3)),
				str(round(obj.q_in_sp, 3)),
				str(round(obj.q_in_sp + 0.05*obj.delta_q, 3)),
				str(round(obj.q_in_sp - 0.05*obj.delta_q, 3)),
				str(round(obj.q_in_sp - 0.378*obj.delta_q, 3)),
				str(round(obj.q_in_sp - 0.10*obj.delta_q, 3)),
				str(round(obj.p_actual_hv, 3)),
				str(round(obj.q_actual_hv, 3))
			])
