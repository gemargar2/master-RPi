import zmq
import math
import json
from time import sleep
from distribution import *

printMessages = False

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
	var1 = ppc_master_obj.p_actual_hv #*ppc_master_obj.S_nom
	var2 = ppc_master_obj.q_actual_hv #*ppc_master_obj.S_nom
	message1 = { "destination": "localPlatform", "value_name": "active_power_HV", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "reactive_power_HV", "value": str(var2) }
	message3 = { "destination": "localPlatform", "value_name": "frequency_HV", "value": str(ppc_master_obj.f_actual) }
	# Calculate current
	if ppc_master_obj.v_actual > 0:
		I = math.sqrt(ppc_master_obj.p_actual_hv**2 + ppc_master_obj.q_actual_hv**2)/ppc_master_obj.v_actual
	else:
		I = 0
	I = I*ppc_master_obj.S_nom/0.15 # MVA/MV = A
	V = ppc_master_obj.v_actual*150
	message4 = { "destination": "localPlatform", "value_name": "current_HV", "value": str(I) }
	message5 = { "destination": "localPlatform", "value_name": "voltage_HV", "value": str(V) }
	if ppc_master_obj.p_actual_hv == 0: PF = 1
	else: PF = math.cos(math.atan(ppc_master_obj.q_actual_hv/ppc_master_obj.p_actual_hv))
	message6 = { "destination": "localPlatform", "value_name": "power_factor_HV", "value": str(PF) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message5, zmq.NOBLOCK)
        	# ppc_master_obj.socket_tx.send_json(message6, zmq.NOBLOCK)
	except:
		print('HV quantities Error')

# --- Running setpoints --------------------------------------

def send_actual_setpoints(ppc_master_obj):
	var1 = ppc_master_obj.p_ex_sp*ppc_master_obj.S_nom
	var2 = ppc_master_obj.q_ex_sp*ppc_master_obj.S_nom
	message1 = { "destination": "localPlatform", "value_name": "actual_P_setpoint", "value": str(var1) }
	message2 = { "destination": "localPlatform", "value_name": "actual_Q_setpoint", "value": str(var2) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
	except:
		print('Actual setpoints Error')


# --- TSO setpoints -----------------------------------------

def send_remote_setpoints(ppc_master_obj):
	var1 = ppc_master_obj.remote_P_sp*ppc_master_obj.S_nom
	var2 = ppc_master_obj.remote_Q_sp*ppc_master_obj.S_nom
	var3 = ppc_master_obj.remote_PF_sp
	var4 = ppc_master_obj.remote_V_sp*ppc_master_obj.V_nom
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
	# var1 = ppc_master_obj.max_P_cap*ppc_master_obj.S_nom
	var1 = ppc_master_obj.S_nom
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
	message6 = { "destination": "localPlatform", "value_name": "main_switch_position", "value": str(ppc_master_obj.main_switch_pos) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message5, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message6, zmq.NOBLOCK)
	except:
        	print('Operation status Error')

# --- Meteo --------------------------------------------------

def send_meteo(ppc_master_obj):
	message1 = { "destination": "localPlatform", "value_name": "temperature", "value": str(round(ppc_master_obj.temp, 2)) }
	message2 = { "destination": "localPlatform", "value_name": "total_irradiance", "value": str(round(ppc_master_obj.irradiance, 2)) }
	message3 = { "destination": "localPlatform", "value_name": "sunrise", "value": str(ppc_master_obj.sunrise) }
	message4 = { "destination": "localPlatform", "value_name": "sunset", "value": str(ppc_master_obj.sunset) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
	except:
        	print('Meteo Error')

# --- TSO --------------------------------------------------

def send_TSO(ppc_master_obj):
	message1 = { "destination": "TSO", "value_name": "L_R", "value": str(ppc_master_obj.local_remote) }
	message2 = { "destination": "TSO", "value_name": "WDOG", "value": str(round(ppc_master_obj.irradiance, 2)) }
	message3 = { "destination": "TSO", "value_name": "HLIM", "value": str(ppc_master_obj.sunrise) }
	message4 = { "destination": "TSO", "value_name": "LLIM", "value": str(ppc_master_obj.sunset) }
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message3, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message4, zmq.NOBLOCK)
	except:
		print('TSO Error')

def transmit_signals(ppc_master_obj, window_obj):
	while True:
		sleep(0.1)
		send_MV_quantities(ppc_master_obj)
		send_HV_quantities(ppc_master_obj)
		send_actual_setpoints(ppc_master_obj)
		send_remote_setpoints(ppc_master_obj)
		send_max_capability(ppc_master_obj)
		send_operation_status(ppc_master_obj)
		send_meteo(ppc_master_obj)
		send_TSO(ppc_master_obj)
		send_internal_setpoints(ppc_master_obj, window_obj)
		send_external_setpoints(ppc_master_obj)
