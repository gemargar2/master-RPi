import threading
from signals_rx import *
from signals_tx import *
from controller_core import *
from class_def import *
from window import *
from time import sleep
from testbench import test_app

plotFlag = True
sampling_period = 0.1

def controller_loop(ppc_master_obj, window_obj):
	while True:
		ppc_master_obj.x = ppc_master_obj.sample*sampling_period
		ppc_master_obj.x_data.append(ppc_master_obj.x)
		# start = time.time()
		controllerCore(window_obj, ppc_master_obj)
		# stop = time.time()
		# control_eta = stop-start
		# print(f'control eta = {control_eta}')
		sleep(sampling_period)
		ppc_master_obj.sample += 1

def main():
	# Configuration file = initialize PPC
	with open('configfile.json', 'r') as openfile:
		config = json.load(openfile)

	# Configuration file = initialize PPC
	with open('memory.json', 'r') as openfile:
		memory = json.load(openfile)
	
	# Wait a sec to finish reading from memory.json	
	sleep(1)
	
	# Create objects
	ppc_master_obj = PPC_master_class(config, memory)
	window_obj = Window_class()
	
	# Start parallel processes
	receive_messages = threading.Thread(target = receive_signals, args=(ppc_master_obj, window_obj))
	receive_messages.start()
	send_messages = threading.Thread(target = transmit_signals, args=(ppc_master_obj, window_obj))
	send_messages.start()
	control = threading.Thread(target = controller_loop, args=(ppc_master_obj, window_obj))
	control.start()
	testApp = threading.Thread(target = test_app, args=(ppc_master_obj, ))
	testApp.start()
	
	# Plot the 5 grid-forming control curves
	window_obj.plot_PF_curve(ppc_master_obj)
	window_obj.plot_QP_curve(ppc_master_obj)
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)
	window_obj.plot_QU_limit_curve(ppc_master_obj)
	
	# Start looping controller core
	while True:
		if plotFlag:
			#start = time.time()
			window_obj.plot_data(ppc_master_obj)	
			#stop = time.time()
			#plot_time_elapsed = stop-start
			#print(f'plot = {plot_time_elapsed}')

if __name__ == "__main__":
	main()


