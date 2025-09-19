import zmq
from local_callbacks import *
from remote_callbacks import *
from distribution import *
from time import sleep

def receive_signals(ppc_master_obj, window_obj):
	while True:
        	# Wait for command
		message = ppc_master_obj.socket_rx.recv_json()
		# print(message)
		
		# Check for local / remote signal
		if message['origin'] == 'localPlatform':
			if message['value_name'] == 'Local_Remote':
				# print(message)
				ppc_master_obj.local_remote = int(message['value'])
			if ppc_master_obj.local_remote == 0: window_obj.fig.suptitle('Master PPC: Local')
			else: window_obj.fig.suptitle('Master PPC: Remote')
		
		# Local mode - only SCADA commands are taken into account
		if ppc_master_obj.local_remote == 0:
			if message['origin'] == 'TSO':
				print("You are in local mode - TSO messages are ignored")
				pass
		
			elif message['origin'] == 'localPlatform':
				# print(message)
				# ----------------------------- mode selection ------------------------------------------------------------
				if message['value_name'] == 'active_control_mode': ppc_master_obj.p_mode = int(message['value'])
				elif message['value_name'] == 'reactive_control_mode': ppc_master_obj.q_mode = int(message['value'])
				# ----------------------------- Local setpoint values  ------------------------------------------------------------
				elif message['value_name'] == 'P_setpoint': local_P_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'Q_setpoint': local_Q_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'PF_setpoint': local_PF_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'V_setpoint': local_V_setpoint(ppc_master_obj, window_obj, float(message['value']))
				# ----------------------------- Universal setpoint values  ------------------------------------------------------------
				elif message['value_name'] == 's_setpoint': local_s_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 's_LFSM_O_setpoint': local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 's_LFSM-U_setpoint': local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'slope_setpoint': local_slope_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'V_deadband_setpoint': local_V_deadband_setpoint(ppc_master_obj, window_obj, float(message['value']))
				# ----------------------------- Gradient values -------------------------------------------------------------
				elif message['value_name'] == 'P_control_gradient': local_P_gradient_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'F_control_gradient': local_F_gradient_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'MPPT_control_gradient': local_MPPT_gradient_setpoint(ppc_master_obj, float(message['value']))
				# ----------------------------- P control PID parameter values ---------------------------------
				elif message['value_name'] == 'Kp_Pcontrol': local_P_Kp(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ki_Pcontrol': local_P_Ki(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Kd_Pcontrol': local_P_Kd(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ti_Pcontrol': local_P_dt(ppc_master_obj, float(message['value']))
				# ----------------------------- P control PID parameter values ---------------------------------
				elif message['value_name'] == 'Kp_Qcontrol': local_Q_Kp(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ki_Qcontrol': local_Q_Ki(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Kd_Qcontrol': local_Q_Kd(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ti_Qcontrol': local_Q_dt(ppc_master_obj, float(message['value']))
				# ----------------------------- Controls -------------------------------------------------------------------
				elif message['value_name'] == 'Stop': stop_command(ppc_master_obj, window_obj)
				elif message['value_name'] == 'Start': start_command(ppc_master_obj, window_obj) # start_command(ppc_master_obj)
				elif message['value_name'] == 'Auto_Start_command': ppc_master_obj.auto_start_state = int(message['value'])
				# ----------------------------- Simulation mode ------------------------------------------------------------
				elif message['value_name'] == 'Simulation_mode_command': ppc_master_obj.simulation_mode = int(message['value'])
				elif message['value_name'] == 'simulation_run_stop': ppc_master_obj.run_simulation(int(message['value']))
				elif message['value_name'] == 'voltage_disturbance': ppc_master_obj.v_disturbance = float(message['value'])
				elif message['value_name'] == 'frequency_disturbance': ppc_master_obj.f_disturbance = float(message['value'])
				elif message['value_name'] == 'simulation_duration': ppc_master_obj.simulation_duration = int(float(message['value']))
	
		# Remote mode - only TSO commands are taken into account - SCADA can still change mode to local
		elif ppc_master_obj.local_remote == 1:
			if message['origin'] == 'localPlatform':
				# print("You are in remote mode - SCADA messages are ignored (except for local_remote)")
				pass

			elif message['origin'] == 'TSO':
				# print(message)
				if message['value_name'] == 'SPMAX': remote_spmax(ppc_master_obj)
				elif message['value_name'] == 'P_SP_TSO': remote_P_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'Q_SP_TSO': remote_Q_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'V_SP_TSO': remote_V_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'PF_SP_TSO': remote_PF_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'ENAP': remote_enap(ppc_master_obj, window_obj)
				elif message['value_name'] == '10': remote_10min(ppc_master_obj, window_obj)

			elif message['origin'] == 'FOSE':
				# print(message)
				if message['value_name'] == 'SPMAX': remote_spmax(ppc_master_obj)
				elif message['value_name'] == 'P_SP_FOSE': fose_P_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'Q_SP_FOSE': fose_Q_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'V_SP_FOSE': fose_V_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'PF_SP_FOSE': fose_PF_setpoint(ppc_master_obj, window_obj, float(message["value"]))
				elif message['value_name'] == 'ENAP': remote_enap(ppc_master_obj, window_obj)
				elif message['value_name'] == '10': remote_10min(ppc_master_obj, window_obj)

		if message['origin'] == 'Slave_1':
			if message['value_name'] == 'Total_Pmax_available': ppc_master_obj.slave_pmax[0] = float(message["value"])
			if message['value_name'] == 'Total_Qmax_available': ppc_master_obj.slave_qmax[0] = float(message["value"])
			if message['value_name'] == 'Total_Qmin_available': ppc_master_obj.slave_qmin[0] = float(message["value"])
			recalc_contribution(ppc_master_obj, window_obj)

		elif message['origin'] == 'Slave_2':
			if message['value_name'] == 'Total_Pmax_available': ppc_master_obj.slave_pmax[1] = float(message["value"])
			if message['value_name'] == 'Total_Qmax_available': ppc_master_obj.slave_qmax[1] = float(message["value"])
			if message['value_name'] == 'Total_Qmin_available': ppc_master_obj.slave_qmin[1] = float(message["value"])
			recalc_contribution(ppc_master_obj, window_obj)	

		elif message['origin'] == 'HV_Meter':
			# print(message)
			if message['value_name'] == 'VAC_ph': ppc_master_obj.v_actual = float(message["value"])
			elif message['value_name'] == 'f': ppc_master_obj.f_actual = float(message["value"])
			elif message['value_name'] == 'Pa': ppc_master_obj.p_actual_hv = float(message["value"])/ppc_master_obj.S_nom
			elif message['value_name'] == 'Qa': ppc_master_obj.q_actual_hv = float(message["value"])/ppc_master_obj.S_nom
			elif message['value_name'] == 'main_switch_position': ppc_master_obj.main_switch_pos = int(message["value"])

