import json
import time
import threading
from limit import *

def local_remote_func(ppc_master_obj, var):
	ppc_master_obj.local_remote = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_remote"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

# ----------------------- Local setpoints ------------------------------------

def local_P_setpoint(ppc_master_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.local_sp.P_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_sp"]["local_P_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update active setpoints
	ppc_master_obj.setpoint_priority()
 
def local_Q_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.local_sp.Q_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_sp"]["local_Q_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update active setpoints
	ppc_master_obj.setpoint_priority()
	# Update corresponding plots
	window_obj.plot_QU_limit_curve(ppc_master_obj)

def local_PF_setpoint(ppc_master_obj, var):
	# Set new setpoint
	ppc_master_obj.local_sp.PF_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_sp"]["local_PF_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update active setpoints
	ppc_master_obj.setpoint_priority()

def local_V_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.V_nom
	# Update ppc_master_obj variable
	ppc_master_obj.local_sp.V_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["local_sp"]["local_V_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update active setpoints
	ppc_master_obj.setpoint_priority()
	# Update corresponding plots
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)

# -------------- Characteristic curves parameters -----------------------------------------

def local_s_setpoint(ppc_master_obj, window_obj, var):
	# Convert % to percentage
	var = var/100
	# Update ppc_master_obj variable
	ppc_master_obj.s_FSM = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["P(f)_curve"]["s_FSM"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update corresponding plots
	window_obj.plot_FSM_curve(ppc_master_obj)

def local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, var):
	# Convert % to percentage
	var = var/100
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_O = var
	ppc_master_obj.memory["P(f)_curve"]["s_LFSM_O"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, var):
	# Convert % to percentage
	var = var/100
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_U = var
	ppc_master_obj.memory["P(f)_curve"]["s_LFSM_U"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def local_slope_setpoint(ppc_master_obj, window_obj, var):
	# Convert % to percentage
	var = var/100
	# Update ppc_master_obj variable
	ppc_master_obj.slope_sp = var
	ppc_master_obj.memory["V_control_curve"]["slope_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update corresponding plots
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)

def local_V_deadband_setpoint(ppc_master_obj, window_obj, var):
	# Convert % to percentage
	var = var/100
	# Update ppc_master_obj variable
	ppc_master_obj.V_deadband_sp = var
	ppc_master_obj.memory["V_control_curve"]["V_deadband_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# Update corresponding plots
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)

# ----------------- Power Gradients ------------------------------------

def local_P_gradient_setpoint(ppc_master_obj, var):
	# Convert MW/sec to p.u/sec = MW/S_nominal
	# var = var/ppc_master_obj.S_nom
	# Check if gradient is within the accepted limits 0.33%/sec < gradient < 0.66%/sec
	#if var > 0.0066: var = 0.0066
	#elif var < 0.0033: var = 0.0033
	# Store into class variable
	ppc_master_obj.P_grad = var
	# Store into memory.json
	ppc_master_obj.memory["power_gradients"]["P_grad"] = round(var, 6)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def local_F_gradient_setpoint(ppc_master_obj, var):
	# Convert MW/sec to p.u/sec = MW/S_nominal
	# var = var/ppc_master_obj.S_nom
	# Check if gradient is within the accepted limits 0.33%/sec < gradient < 0.66%/sec
	#if var > 0.0066: var = 0.0066
	#elif var < 0.0033: var = 0.0033
	# Store into class variable
	ppc_master_obj.F_grad = var
	# Store into memory.json
	ppc_master_obj.memory["power_gradients"]["F_grad"] = round(var, 6)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def local_MPPT_gradient_setpoint(ppc_master_obj, var):
	# Convert MW/sec to p.u/sec = MW/S_nominal
	# var = var/ppc_master_obj.S_nom
	# Check if gradient is within the accepted limits 0.33%/sec < gradient < 0.66%/sec
	#if var > 0.0066: var = 0.0066
	#elif var < 0.0033: var = 0.0033
	# Store to class variable
	ppc_master_obj.MPPT_grad = var
	ppc_master_obj.memory["power_gradients"]["MPPT_grad"] = round(var, 6)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

# ---------------- P PID parameters ------------------------------------

def set_p_kp(ppc_master_obj, var):
	ppc_master_obj.p_pid.kp = var
	# Store into memory.json
	ppc_master_obj.memory["P_PID_parameters"]["p_kp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def set_p_ki(ppc_master_obj, var):
	ppc_master_obj.p_pid.ki = var
	# Store into memory.json
	ppc_master_obj.memory["P_PID_parameters"]["p_ki"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
		
def set_p_kd(ppc_master_obj, var):
	ppc_master_obj.p_pid.kd = var
	# Store into memory.json
	ppc_master_obj.memory["P_PID_parameters"]["p_kd"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def set_p_dt(ppc_master_obj, var):
	ppc_master_obj.p_pid.dt = var
	# Store into memory.json
	ppc_master_obj.memory["P_PID_parameters"]["p_dt"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

# ---------------- Q PID parameters ------------------------------------

def set_q_kp(ppc_master_obj, var):
	ppc_master_obj.q_pid.kp = var
	# Store into memory.json
	ppc_master_obj.memory["Q_PID_parameters"]["q_kp"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def set_q_ki(ppc_master_obj, var):
	ppc_master_obj.q_pid.ki = var
	# Store into memory.json
	ppc_master_obj.memory["Q_PID_parameters"]["q_ki"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
		
def set_q_kd(ppc_master_obj, var):
	ppc_master_obj.q_pid.kd = var
	# Store into memory.json
	ppc_master_obj.memory["Q_PID_parameters"]["q_kd"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

def set_q_dt(ppc_master_obj, var):
	ppc_master_obj.q_pid.dt = var
	# Store into memory.json
	ppc_master_obj.memory["Q_PID_parameters"]["q_dt"] = var
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)

#  --------------- TSO Setpoints -------------------------------------

def tso_P_setpoint(ppc_master_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.tso_sp.P_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["tso_setpoints"]["tso_P_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()

def tso_Q_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.tso_sp.Q_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["tso_setpoints"]["tso_Q_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()
	window_obj.plot_QU_limit_curve(ppc_master_obj)

def tso_PF_setpoint(ppc_master_obj, var):
	# Set new setpoint
	ppc_master_obj.tso_sp.PF_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["tso_setpoints"]["tso_PF_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()

def tso_V_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.V_nom
	# Update ppc_master_obj variable
	ppc_master_obj.tso_sp.V_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["tso_setpoints"]["tso_V_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)

#  --------------- FOSE Setpoints ------------------------------------

def fose_P_setpoint(ppc_master_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.fose_sp.P_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["fose_setpoints"]["fose_P_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()

def fose_Q_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.S_nom
	# Update ppc_master_obj variable
	ppc_master_obj.fose_sp.Q_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["fose_setpoints"]["fose_Q_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()
	window_obj.plot_QU_limit_curve(ppc_master_obj)

def fose_PF_setpoint(ppc_master_obj, var):
	# Set new setpoint
	ppc_master_obj.fose_sp.PF_sp = var
	# Store the last setpoint to memory
	ppc_master_obj.memory["fose_setpoints"]["fose_PF_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()

def fose_V_setpoint(ppc_master_obj, window_obj, var):
	# Convert to p.u
	var = var/ppc_master_obj.V_nom
	# Update ppc_master_obj variable
	ppc_master_obj.fose_sp.V_sp = var # store as per-unit
	# Store the last setpoint to memory
	ppc_master_obj.memory["fose_setpoints"]["fose_V_sp"] = round(var, 3)
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	ppc_master_obj.setpoint_priority()
	window_obj.plot_V_control_curve(ppc_master_obj)
	window_obj.plot_QU_curve(ppc_master_obj)

# ----------------- TSO special functions ------------------------------------

def stop_command(ppc_master_obj, window_obj, var):
	print(f"Stop command: {var}")
	# ppc_master_obj.operational_state = var
	if var == 1:
		ppc_master_obj.start_stop = 0
		ppc_master_obj.operational_state = 1
	else:
		ppc_master_obj.start_stop = 1
		# Check if frequency and voltage are within limits
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
	stop_command(ppc_master_obj, window_obj, 1)

def remote_10min(ppc_master_obj, window_obj):
	window_obj.fig.suptitle('Master PPC: Shutdown in 10 minutes')
	t1 = threading.Thread(target = routine_10min, args=(ppc_master_obj, window_obj))
	t1.start()
