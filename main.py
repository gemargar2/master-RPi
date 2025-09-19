import threading
from signals_rx import *
from signals_tx import *
from controller_core import *
from class_def import *
from limit import *

def main():
	with open('configfile.json', 'r') as openfile:
		config = json.load(openfile)

	# Create objects
	ppc_master_obj = PPC_master_class(config)
	window_obj = Window_class()

	# Start parallel processes
	# Scans Tsotakis IP for signals comming from SCADA
	receive_messages = threading.Thread(target = receive_signals, args=(ppc_master_obj, window_obj))
	receive_messages.start()
	send_messages = threading.Thread(target = transmit_signals, args=(ppc_master_obj, window_obj))
	send_messages.start()

	# Initialize Q-U with limit curve
	ppc_master_obj.V_Limit_VDE_init(q_ref=0.0)
	ppc_master_obj.QP_init()
	window_obj.plot_PF_curve(ppc_master_obj)
	window_obj.plot_QP_curve(ppc_master_obj)
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)
	window_obj.plot_QU_limit_curve(ppc_master_obj)

	# Start looping controller core
	i = 0
	while True:
		controllerCore(i, window_obj, ppc_master_obj)
		i += 1

if __name__ == "__main__":
	main()


