import json
from time import sleep
import threading

# Remote commands

def stop_command(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Shutdown complete')
	ppc_master_obj.operational_state = 1

def start_command(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Local')
	ppc_master_obj.operational_state = 0

def routine_10min(ppc_master_obj, window_obj):
	ppc_master_obj.operational_state = 2
	for counter in range(0,10):
		window_obj.fig.suptitle(u"Master PPC: Shutdown in {} seconds".format(10-counter))
		sleep(1)
	stop_command(ppc_master_obj, window_obj)

# Fose setpoints

def fose_P_setpoint(ppc_master_obj, window_obj, var):
	pass

def fose_Q_setpoint(ppc_master_obj, window_obj, var):
	pass
    
# Remote setpoints

def remote_P_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.remote_P_sp = var/ppc_master_obj.S_nom
	ppc_master_obj.memory["remote_P_sp"] = var
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)
	# Update setpoint json file
	with open("setpoints.json", "w") as outfile:
		json.dump(ppc_master_obj.memory, outfile)

def remote_Q_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.remote_Q_sp = var/ppc_master_obj.S_nom
	ppc_master_obj.memory["remote_Q_sp"] = var
	# Update plots
	window_obj.plot_QU_limit_curve(ppc_master_obj)
	# Update setpoint json file
	with open("setpoints.json", "w") as outfile:
		json.dump(ppc_master_obj.memory, outfile)

def remote_PF_setpoint(ppc_master_obj, var):
	ppc_master_obj.remote_PF_sp = var
	ppc_master_obj.memory["remote_PF_sp"] = var
	with open("setpoints.json", "w") as outfile:
		json.dump(ppc_master_obj.memory, outfile)

def remote_V_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.remote_V_sp = var/ppc_master_obj.V_nom
	ppc_master_obj.memory["remote_V_sp"] = var
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)
	# Update setpoint json file
	with open("setpoints.json", "w") as outfile:
		json.dump(ppc_master_obj.memory, outfile)

# TSO commands

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

