import zmq
import math
import json
import time
from distribution import *

printMessages = False

# --- localPlatform -------------------------------------------

# --- MV quantities -------------------------------------------

def send_MV_quantities(ppc_master_obj):
	var1 = ppc_master_obj.p_actual_mv * ppc_master_obj.S_nom
	var2 = ppc_master_obj.q_actual_mv * ppc_master_obj.S_nom
	message1 = { "destination": "localPlatform", "value_name": "active_power_MV", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "reactive_power_MV", "value": str(var2) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
	except:
		print('MV quantities Error')

# --- HV quantities -------------------------------------------

def send_HV_quantities(ppc_master_obj):
	var1 = ppc_master_obj.hv_meter.p_actual* ppc_master_obj.S_nom
	var2 = ppc_master_obj.hv_meter.q_actual * ppc_master_obj.S_nom
	f_value = ppc_master_obj.hv_meter.f_actual
	v_value = ppc_master_obj.hv_meter.v_actual * 150
	message1 = { "destination": "localPlatform", "value_name": "active_power_HV", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "reactive_power_HV", "value": str(var2) }	
	message3 = { "destination": "localPlatform", "value_name": "frequency_HV", "value": str(f_value) }
	# Calculate current
	if v_value > 0: I = math.sqrt(ppc_master_obj.hv_meter.p_actual**2 + ppc_master_obj.hv_meter.q_actual**2)/v_value
	else: I = 0
	I = I*ppc_master_obj.S_nom/0.15 # MVA/MV = A
	message4 = { "destination": "localPlatform", "value_name": "current_HV", "value": str(I) }
	message5 = { "destination": "localPlatform", "value_name": "voltage_HV", "value": str(v_value) }
	message6 = { "destination": "localPlatform", "value_name": "PF", "value": str(ppc_master_obj.hv_meter.pf_actual) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message5, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message6, zmq.NOBLOCK)
	except:
		print('HV quantities Error')

# --- Running setpoints --------------------------------------

def send_actual_setpoints(ppc_master_obj):
	var1 = ppc_master_obj.p_in_sp * ppc_master_obj.S_nom
	var2 = ppc_master_obj.q_in_sp * ppc_master_obj.S_nom
	message1 = { "destination": "localPlatform", "value_name": "actual_P_setpoint", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "actual_Q_setpoint", "value": str(var2) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
	except:
		print('Actual setpoints Error')


# --- TSO setpoints -----------------------------------------

def send_remote_setpoints(ppc_master_obj):
	var1 = ppc_master_obj.remote_sp.P_sp * ppc_master_obj.S_nom
	var2 = ppc_master_obj.remote_sp.Q_sp * ppc_master_obj.S_nom
	var3 = ppc_master_obj.remote_sp.PF_sp
	var4 = ppc_master_obj.remote_sp.V_sp * ppc_master_obj.V_nom
	message1 = { "destination": "localPlatform", "value_name": "P_setpoint_remote", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "Q_setpoint_remote", "value": str(var2) }
	message3 = { "destination": "localPlatform", "value_name": "PF_setpoint_remote", "value": str(var3) }
	message4 = { "destination": "localPlatform", "value_name": "V_setpoint_remote", "value": str(var4) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
	except:
		print('Remote setpoints Error')

# --- Max capability base on meteo ---------------------------

def send_max_capability(ppc_master_obj):
	var1 = ppc_master_obj.max_P_cap*ppc_master_obj.S_nom
	var2 = ppc_master_obj.max_Q_cap*ppc_master_obj.S_nom
	var3 = ppc_master_obj.min_Q_cap*ppc_master_obj.S_nom
	message1 = { "destination": "localPlatform", "value_name": "max_active_capability", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "max_reactive_capability", "value": str(var2) }
	message3 = { "destination": "localPlatform", "value_name": "min_Q_capability", "value": str(var3) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
	except:
		print('Max capability Error')

# --- Modes of operation -------------------------------------

def send_operation_status(ppc_master_obj):
	message1 = { "destination": "localPlatform", "value_name": "P_control_mode", "value": str(ppc_master_obj.p_mode) }
	message2 = { "destination": "localPlatform", "value_name": "Q_control_mode", "value": str(ppc_master_obj.q_mode) }
	message3 = { "destination": "localPlatform", "value_name": "simulation_start_stop", "value": str(ppc_master_obj.simulation_start_stop) }
	message4 = { "destination": "localPlatform", "value_name": "operational_state", "value": str(ppc_master_obj.operational_state) }
	message5 = { "destination": "localPlatform", "value_name": "Auto_Start_state", "value": str(ppc_master_obj.auto_start_state) }
	message6 = { "destination": "localPlatform", "value_name": "main_switch_position", "value": str(ppc_master_obj.hv_meter.main_switch_pos) }
	message7 = { "destination": "localPlatform", "value_name": "Local_Remote", "value": str(ppc_master_obj.local_remote) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message5, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message6, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message7, zmq.NOBLOCK)
	except:
        	print('Operation status Error')

# --- Meteo --------------------------------------------------

def send_meteo(ppc_master_obj):
	message1 = { "destination": "localPlatform", "value_name": "temperature", "value": str(round(ppc_master_obj.temp, 2)) }
	message2 = { "destination": "localPlatform", "value_name": "total_irradiance", "value": str(round(ppc_master_obj.irradiance, 2)) }
	# message3 = { "destination": "localPlatform", "value_name": "sunrise", "value": str(sunrise) }
	# message4 = { "destination": "localPlatform", "value_name": "sunset", "value": str(sunset) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		# ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		# ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
	except:
        	print('Meteo Error')

# --- TSO --------------------------------------------------

def send_TSO(ppc_master_obj):
	message1 = { "destination": "TSO", "value_name": "L_R", "value": str(ppc_master_obj.local_remote) }
	message2 = { "destination": "TSO", "value_name": "WDOG", "value": str(ppc_master_obj.watchdog) }
	message3 = { "destination": "TSO", "value_name": "HLIM", "value": str(ppc_master_obj.total_pmax) }
	message4 = { "destination": "TSO", "value_name": "LLIM", "value": "0" }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
	except:
		print('TSO Error')

# --- Write into memory -------------------------------------------

def memory_write(ppc_master_obj):
	# start = time.time()
	# Store the last setpoint to memory
	ppc_master_obj.memory["internal_setpoints"]["p_in_sp"] = round(ppc_master_obj.p_in_sp, 3)
	ppc_master_obj.memory["internal_setpoints"]["q_in_sp"] = round(ppc_master_obj.q_in_sp, 3)
	# Gradient submodule
	ppc_master_obj.memory["internal_setpoints"]["p_grad_sp"] = round(ppc_master_obj.grad_submod.p.output, 3)
	ppc_master_obj.memory["internal_setpoints"]["q_grad_sp"] = round(ppc_master_obj.grad_submod.q.output, 3)
	ppc_master_obj.memory["internal_setpoints"]["prev_p_grad_sp"] = round(ppc_master_obj.grad_submod.p.prev_state, 3)
	ppc_master_obj.memory["internal_setpoints"]["prev_q_grad_sp"] = round(ppc_master_obj.grad_submod.q.prev_state, 3)
	# PID submodule
	ppc_master_obj.memory["internal_setpoints"]["p_pid_sp"] = round(ppc_master_obj.pid_submod.p.output, 3)
	ppc_master_obj.memory["internal_setpoints"]["q_pid_sp"] = round(ppc_master_obj.pid_submod.q.output, 3)
	ppc_master_obj.memory["internal_setpoints"]["prev_p_pid_sp"] = round(ppc_master_obj.pid_submod.p.prev_state, 3)
	ppc_master_obj.memory["internal_setpoints"]["prev_q_pid_sp"] = round(ppc_master_obj.pid_submod.q.prev_state, 3)
	# Mode selection
	ppc_master_obj.memory["control_mode"]["active_control_mode"] = ppc_master_obj.p_mode
	ppc_master_obj.memory["control_mode"]["reactive_control_mode"] = ppc_master_obj.q_mode
	with open("memory.json", "w") as f:
		json.dump(ppc_master_obj.memory, f)
	# end = time.time()
	# eta = end-start
	# print(f'memory write eta = {eta}')


# --- Loop -------------------------------------------

def transmit_signals(ppc_master_obj, window_obj):
	while True:
		time.sleep(0.1)
		# send data to SCADA
		send_MV_quantities(ppc_master_obj)
		send_HV_quantities(ppc_master_obj)
		send_actual_setpoints(ppc_master_obj)
		send_remote_setpoints(ppc_master_obj)
		send_max_capability(ppc_master_obj)
		send_operation_status(ppc_master_obj)
		send_meteo(ppc_master_obj)
		send_TSO(ppc_master_obj)
		send_external_setpoints(ppc_master_obj)
		# Send setpoints to slave PPCs
		send_internal_setpoints(ppc_master_obj, window_obj)
		# Write current setpoints to memory json
		memory_write(ppc_master_obj)
