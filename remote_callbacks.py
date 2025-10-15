import json
from time import sleep
import threading

# Remote commands

def stop_command(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Shutdown complete')
	ppc_master_obj.operational_state = 1

def start_command(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Local')
	if ppc_master_obj.start_enable == True:
		ppc_master_obj.rehab = False
		ppc_master_obj.operational_state = 0
	else: print("Problem! PPC can't start")

def routine_10min(ppc_master_obj, window_obj):
	ppc_master_obj.operational_state = 2
	for counter in range(0,10):
		window_obj.fig.suptitle(u"Master PPC: Shutdown in {} seconds".format(10*60-counter))
		sleep(1)
	stop_command(ppc_master_obj, window_obj)

def remote_spmax(ppc_master_obj):
	print("SPMAX")
	ppc_master_obj.p_mode = 3

def remote_enap(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: ENAP (Emergency shutdown)')
	stop_command(ppc_master_obj, window_obj)

def remote_10min(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Shutdown in 10 minutes')
	t1 = threading.Thread(target = routine_10min, args=(ppc_master_obj, window_obj))
	t1.start()

