import zmq
import json

printMessages = False

# Recalculate slaves contribution based on real time active power availability
def recalc_contribution(ppc_master_obj, window_obj):
	# Calculate new available
	new_checksum = 0
	for i in range(ppc_master_obj.numberOfSlaves):
		new_checksum += ppc_master_obj.pmax_avail[i]

	# for i in range(ppc_master_obj.numberOfSlaves):
	#	ppc_master_obj.contribution[i] = ppc_master_obj.pmax_avail[i]/new_checksum
    
	# Master 
	production = round(ppc_master_obj.P_nom * ppc_master_obj.p_actual_hv, 2)
	setpoint = round(ppc_master_obj.P_nom * ppc_master_obj.p_ex_sp, 2)
	available = round(new_checksum, 2)
	installed = round(ppc_master_obj.P_nom, 2)
	# Slave 1
	slave1_contribution = int(ppc_master_obj.contribution[0]*100)
	slave1_setpoint = round(ppc_master_obj.P_nom * ppc_master_obj.slave_p_sp[0], 2)
	slave1_available = round(ppc_master_obj.pmax_avail[0], 2)
	slave1_installed = round(ppc_master_obj.p_installed[0], 2)
	# Slave 2
	slave2_contribution = int(ppc_master_obj.contribution[1]*100)
	slave2_setpoint =  round(ppc_master_obj.P_nom * ppc_master_obj.slave_p_sp[1], 2)
	slave2_available = round(ppc_master_obj.pmax_avail[1], 2)
	slave2_installed = round(ppc_master_obj.p_installed[1], 2)

	master_str = f'Master P={production} / S={setpoint} / A={available} / I={installed}'
	slave1_str = f'Slave 1 ({slave1_contribution}%) P={slave1_setpoint} / A={slave1_available} / I={slave1_installed}'
	slave2_str = f'Slave 2 ({slave2_contribution}%) P={slave2_setpoint} / A={slave2_available} / I={slave2_installed}'
	if ppc_master_obj.operational_state == 0: window_obj.fig.suptitle(f'{master_str} \n {slave1_str} / {slave2_str}')

# --- SLAVES ------------------------------------------------
def send_internal_setpoints(ppc_master_obj, window_obj):
	recalc_contribution(ppc_master_obj, window_obj)
	for i in range(ppc_master_obj.numberOfSlaves):
		dest = "Slave_" + str(i+1)
		ppc_master_obj.slave_p_sp[i] = ppc_master_obj.p_in_sp * ppc_master_obj.contribution[i]
		ppc_master_obj.slave_q_sp[i] = ppc_master_obj.q_in_sp * ppc_master_obj.contribution[i]
		message1 = {"destination": dest, "value_name": "P_SP_master", "value": str(ppc_master_obj.slave_p_sp[i])}
		message2 = {"destination": dest, "value_name": "Q_SP_master", "value": str(ppc_master_obj.slave_q_sp[i])}
		try:
			ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
			ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
			if printMessages: print("Success")
		except:
			if printMessages: print('Slave internal setpoints Error')

# --- GRID --------------------------------------------------
def send_external_setpoints(ppc_master_obj):
	message1 = {"destination": "Grid", "value_name": "p_ex_sp", "value": str(ppc_master_obj.p_ex_sp * ppc_master_obj.S_nom)}
	message2 = {"destination": "Grid", "value_name": "q_ex_sp", "value": str(ppc_master_obj.q_ex_sp * ppc_master_obj.S_nom)}
	try:
		ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
		ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
		if printMessages: print("Success")
	except:
		if printMessages: print('Grid external setpoint error')

