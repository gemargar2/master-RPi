import json
import math
import time
import threading
from limit import *

# ---------------------------- Local setpoints ------------------------------------

def local_P_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_P_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_setpoints"]["local_P_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
 
def local_Q_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_Q_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_setpoints"]["local_Q_sp"] = var
	with open("memory.json", "w") as f: 
		json.dump(ppc_master_obj.memory, f)
	# Update plots
	window_obj.plot_QU_limit_curve(ppc_master_obj)

def local_PF_setpoint(ppc_master_obj, var):
	# Set new setpoint
	ppc_master_obj.local_PF_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_setpoints"]["local_PF_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def local_V_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_V_sp = var/ppc_master_obj.V_nom
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_setpoints"]["local_V_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)

# Universal setpoints
def local_s_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_FSM = var/100
	# Update plots
	# window_obj.plot_FSM_curve(ppc_master_obj)

def local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_O = var/100
	# Update plotsl
	# window_obj.plot_PF_curve(ppc_master_obj)

def local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_U = var/100
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)

def local_slope_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.slope_sp = var/100
	# Update plots
	# window_obj.plot_QU_curve(ppc_master_obj)

def local_V_deadband_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.V_deadband_sp = var/100
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)

# Gradients
def local_P_gradient_setpoint(ppc_master_obj, var):
	# Convert MW/second to p.u/sample = (MW/S_nominal)/(second/sampling_period) = var/(S_nom*samplig_period)
	ppc_master_obj.P_grad = var/(ppc_master_obj.S_nom*ppc_master_obj.sampling_rate)

def local_F_gradient_setpoint(ppc_master_obj, var):
	ppc_master_obj.F_grad = var/(ppc_master_obj.S_nom*ppc_master_obj.sampling_rate)

def local_MPPT_gradient_setpoint(ppc_master_obj, var):
	ppc_master_obj.MPPT_grad = var/(ppc_master_obj.S_nom*ppc_master_obj.sampling_rate)

# Hello sunshine
def recalc_pf(ppc_master_obj):
	if ppc_master_obj.p_actual_hv == 0:
		ppc_master_obj.pf_actual = 1
	else:
		ppc_master_obj.pf_actual = math.cos(math.atan(ppc_master_obj.q_actual_hv/ppc_master_obj.p_actual_hv))
		# if ppc_master_obj.q_actual_hv < 0: ppc_master_obj.pf_actual = -ppc_master_obj.pf_actual

def settling_time_pf(ppc_master_obj):
	flag = True
	dn = ppc_master_obj.local_PF_sp*0.95
	up = ppc_master_obj.local_PF_sp*1.05
	while(flag):
		print("Tik")
		# Check if external setpoint has changed
		if (ppc_master_obj.pf_actual<up and ppc_master_obj.pf_actual>dn):
			end = time.time()
			diff = end-ppc_master_obj.start
			print(f'settling time is {diff}')
			flag = False
		time.sleep(0.1)
	print("exit")

# ---------------------------- Remote callbacks ------------------------------------

def stop_command(ppc_master_obj, window_obj, var):
	print(f"Stop command: {var}")
	# ppc_master_obj.operational_state = var
	if var == 1:
		ppc_master_obj.start_stop = 0
		ppc_master_obj.operational_state = 1
	else:
		ppc_master_obj.start_stop = 1
		operating_ranges(ppc_master_obj, window_obj)

def routine_10min(ppc_master_obj, window_obj):
	ppc_master_obj.operational_state = 2
	for counter in range(0,10):
		window_obj.fig.suptitle(u"Master PPC: Shutdown in {} seconds".format(10*60-counter))
		time.sleep(1)
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

# Setpoints
def remote_P_setpoint(ppc_master_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.remote_P_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["remote_setpoints"]["remote_P_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def remote_Q_setpoint(ppc_master_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_Q_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["remote_setpoints"]["remote_Q_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def remote_PF_setpoint(ppc_master_obj, var):
	# Set new setpoint
	ppc_master_obj.local_PF_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["remote_setpoints"]["remote_PF_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def remote_V_setpoint(ppc_master_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_V_sp = var/ppc_master_obj.V_nom # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["remote_setpoints"]["remote_V_sp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

