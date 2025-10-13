import threading
from signals_rx import *
from signals_tx import *
from controller_core import *
from class_def import *
from window import *
from logfile import *

plotFlag = True
logFlag = False

def main():
	with open('configfile.json', 'r') as openfile:
		config = json.load(openfile)
	
	# Create objects
	ppc_master_obj = PPC_master_class(config)
	window_obj = Window_class()
	logfile_obj = logFile_class()

	# Start parallel processes
	receive_messages = threading.Thread(target = receive_signals, args=(ppc_master_obj, window_obj))
	receive_messages.start()
	send_messages = threading.Thread(target = transmit_signals, args=(ppc_master_obj, window_obj))
	send_messages.start()
	
	# Plot the 5 grid-forming control curves
	window_obj.plot_PF_curve(ppc_master_obj)
	window_obj.plot_QP_curve(ppc_master_obj)
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)
	window_obj.plot_QU_limit_curve(ppc_master_obj)
	
	# Start looping controller core
	i = 0
	while True:
		controllerCore(i, window_obj, ppc_master_obj)
		if logFlag: logfile_obj.write_data(ppc_master_obj)
		x = i/10 # convert samples to seconds
		if plotFlag: window_obj.plot_data(x, ppc_master_obj)
		else: time.sleep(1/ppc_master_obj.sampling_rate)
		i += 1

if __name__ == "__main__":
	main()


