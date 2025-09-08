import zmq
import json

printMessages = False

# Recalculate slaves contribution based on real time active power availability
def recalc_contribution(ppc_master_obj, window_obj):
	# Recalculate available power yield
	ppc_master_obj.total_pmax = 0
	ppc_master_obj.total_qmax = 0
	ppc_master_obj.total_qmin = 0
	for index in range(ppc_master_obj.numberOfSlaves):
		ppc_master_obj.total_pmax += ppc_master_obj.slave_pmax[index]
		ppc_master_obj.total_qmax += ppc_master_obj.slave_qmax[index]
		ppc_master_obj.total_qmin += ppc_master_obj.slave_qmin[index]	

	# Calculate new contribution
	for index in range(ppc_master_obj.numberOfSlaves):
		ppc_master_obj.pi_per[index] = 0.0
		ppc_master_obj.qi_per[index] = 0.0
		ppc_master_obj.qa_per[index] = 0.0
		if True:
			if ppc_master_obj.total_pmax != 0: ppc_master_obj.pi_per[index] = ppc_master_obj.slave_pmax[index]/ppc_master_obj.total_pmax
			if ppc_master_obj.total_qmax != 0: ppc_master_obj.qi_per[index] = ppc_master_obj.slave_qmax[index]/ppc_master_obj.total_qmax
			if ppc_master_obj.total_qmin != 0: ppc_master_obj.qa_per[index] = ppc_master_obj.slave_qmin[index]/ppc_master_obj.total_qmin
    
	master_r = f'Master({ppc_master_obj.total_pmax}/{ppc_master_obj.total_qmax}/{ppc_master_obj.total_qmin})'
	slave1_r = f'slave1({ppc_master_obj.slave_pmax[0]}/{ppc_master_obj.slave_qmax[0]}/{ppc_master_obj.slave_qmin[0]})'
	slave2_r = f'slave2({ppc_master_obj.slave_pmax[1]}/{ppc_master_obj.slave_qmax[1]}/{ppc_master_obj.slave_qmin[1]})'
	slave1_p = f'slave1({int(ppc_master_obj.pi_per[0]*100)}/{int(ppc_master_obj.qi_per[0]*100)}/{int(ppc_master_obj.qa_per[0]*100)})'
	slave2_p = f'slave2({int(ppc_master_obj.pi_per[1]*100)}/{int(ppc_master_obj.qi_per[1]*100)}/{int(ppc_master_obj.qa_per[1]*100)})'

	if ppc_master_obj.operational_state == 0:
		window_obj.fig.suptitle(f'Availability (MW/MVAR): {master_r}, {slave1_r}, {slave2_r} \n Contribution (%): {slave1_p} {slave2_p}')

# --- SLAVES ------------------------------------------------
def send_internal_setpoints(ppc_master_obj, window_obj):
	# Iterate through slaves
	for i in range(ppc_master_obj.numberOfSlaves):
		dest = "Slave_" + str(i+1)
		# Distribution for p inj, q inj and q abs
		ppc_master_obj.slave_p_sp[i] = ppc_master_obj.p_in_sp * ppc_master_obj.S_nom * ppc_master_obj.pi_per[i]
		if ppc_master_obj.q_in_sp < 0:
			ppc_master_obj.slave_q_sp[i] = ppc_master_obj.q_in_sp * ppc_master_obj.S_nom * ppc_master_obj.qa_per[i]
		else:
			ppc_master_obj.slave_q_sp[i] = ppc_master_obj.q_in_sp * ppc_master_obj.S_nom * ppc_master_obj.qi_per[i]
		# Check limits
		if ppc_master_obj.slave_p_sp[i] > ppc_master_obj.slave_pmax[i]: ppc_master_obj.slave_p_sp[i] = ppc_master_obj.slave_pmax[i]
		if ppc_master_obj.slave_q_sp[i] > ppc_master_obj.slave_qmax[i]: ppc_master_obj.slave_q_sp[i] = ppc_master_obj.slave_qmax[i]
		if ppc_master_obj.slave_q_sp[i] < ppc_master_obj.slave_qmin[i]: ppc_master_obj.slave_q_sp[i] = ppc_master_obj.slave_qmin[i]
		# Send setponts
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

