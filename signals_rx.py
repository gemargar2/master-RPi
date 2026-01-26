import zmq
from callbacks import *
from distribution import *
from time import sleep

printMessages = False

grid_rx = True
tso_rx = True
fose_rx = True
scada_rx = True
hv_meter_rx = True
tso_server_rx = True
slave1_rx = True
slave2_rx = True

def receive_signals(ppc_master_obj, window_obj):
	global grid_rx, tso_rx, fose_rx, scada_rx, hv_meter_rx, tso_server_rx, slave1_rx, slave2_rx
	
	while True:
        	# Wait for command
		message = ppc_master_obj.socket_rx.recv_json()
		# print(message)
		
		origin = ''
		
		# Check for connection status
		if message['value_name'] == 'df925a75-00a7-40ae-8ed9-cb5008d725ce':
			# print(message)
			if message['origin'] == 'Grid':
				origin = 'Grid'
				grid_rx = message['status']
			elif message['origin'] == 'TSO':
				origin = 'TSO'
				tso_rx = message['status']
			elif message['origin'] == 'TSO_server':
				origin = 'TSO_server'
				tso_server_rx = message['status']
			elif message['origin'] == 'FOSE':
				origin = 'FOSE'
				fose_rx = message['status']
			elif message['origin'] == 'localPlatform':
				origin = 'SCADA'
				scada_rx = message['status']
			elif message['origin'] == 'HV_Meter':
				origin = 'HV_Meter'
				hv_meter_rx = message['status']
			elif message['origin'] == 'Slave_1':
				origin = 'Slave_1'
				slave1_rx = message['status']
			elif message['origin'] == 'Slave_2':
				origin = 'Slave_2'
				slave2_rx = message['status']
			else: pass
			
			if message['status'] == True:
				if printMessages: print(f"{message['origin']} connection ok")
			else:
				if printMessages: print(f"{message['origin']} connection not ok")
			
			if grid_rx and tso_rx and fose_rx and scada_rx and hv_meter_rx and slave1_rx and slave2_rx: ppc_master_obj.watchdog = True
			else: ppc_master_obj.watchdog = False
		
		# Check for local / remote signal
		if message['origin'] == 'localPlatform':
			if message['value_name'] == 'Local_Remote': ppc_master_obj.local_remote = int(message['value'])
			if ppc_master_obj.local_remote == 0: window_obj.fig.suptitle('Master PPC: Local')
			else: window_obj.fig.suptitle('Master PPC: Remote')
		
		# Local mode - only SCADA commands are taken into account
		if ppc_master_obj.local_remote == 0:
			if message['origin'] == 'TSO':
				if printMessages: print("You are in local mode - TSO messages are ignored")
				pass
			
			elif message['origin'] == 'localPlatform':
				# ----------------------------- mode selection ------------------------------------------------------------
				if message['value_name'] == 'active_control_mode': ppc_master_obj.p_mode = int(message['value'])
				elif message['value_name'] == 'reactive_control_mode': ppc_master_obj.q_mode = int(message['value'])
				# ----------------------------- Local setpoint values  ------------------------------------------------------------
				elif message['value_name'] == 'P_setpoint': local_P_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'Q_setpoint': local_Q_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'PF_setpoint': local_PF_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'V_setpoint': local_V_setpoint(ppc_master_obj, window_obj, float(message['value']))
				# ----------------------------- Universal seltpoint values  ------------------------------------------------------------
				elif message['value_name'] == 's_setpoint': local_s_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 's_LFSM_O_setpoint': local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 's_LFSM-U_setpoint': local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'slope_setpoint': local_slope_setpoint(ppc_master_obj, window_obj, float(message['value']))
				elif message['value_name'] == 'V_deadband_setpoint': local_V_deadband_setpoint(ppc_master_obj, window_obj, float(message['value']))
				# ----------------------------- Gradient values ------------------------l-------------------------------------
				elif message['value_name'] == 'P_control_gradient': local_P_gradient_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'F_control_gradient': local_F_gradient_setpoint(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'MPPT_control_gradient': local_MPPT_gradient_setpoint(ppc_master_obj, float(message['value']))
				# ----------------------------- P control PID parameter values ---------------------------------
				elif message['value_name'] == 'Kp_Pcontrol': set_p_kp(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ki_Pcontrol': set_p_ki(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Kd_Pcontrol': set_p_kd(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ti_Pcontrol': set_p_dt(ppc_master_obj, float(message['value']))
				# ----------------------------- P control PID parameter values ---------------------------------
				elif message['value_name'] == 'Kp_Qcontrol': set_q_kp(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ki_Qcontrol': set_q_ki(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Kd_Qcontrol': set_q_kd(ppc_master_obj, float(message['value']))
				elif message['value_name'] == 'Ti_Qcontrol': set_q_dt(ppc_master_obj, float(message['value']))
				# ----------------------------- Controls -------------------------------------------------------------------
				elif message['value_name'] == 'Stop': stop_command(ppc_master_obj, window_obj, int(message['value']))
				elif message['value_name'] == 'Start': pass # start_command(ppc_master_obj, window_obj, int(message['value']))
				elif message['value_name'] == 'Auto_Start_command': ppc_master_obj.auto_start_state = int(message['value'])
				# ----------------------------- Simulation mode ----------------------------------l--------------------------
				elif message['value_name'] == 'Simulation_mode_command': ppc_master_obj.simulation_mode = int(message['value'])
				elif message['value_name'] == 'simulation_run_stop': ppc_master_obj.run_simulation(int(message['value']))
				elif message['value_name'] == 'voltage_disturbance': ppc_master_obj.v_disturbance = float(message['value'])
				elif message['value_name'] == 'frequency_disturbance': ppc_master_obj.f_disturbance = float(message['value'])
				elif message['value_name'] == 'simulation_duration': ppc_master_obj.simulation_duration = int(float(message['value']))
		
		# Remote mode - only TSO commands are taken into account - SCADA can still change mode to local
		elif ppc_master_obj.local_remote == 1:
			if message['origin'] == 'localPlatform':
				if printMessages: print("You are in remote mode - SCADA messages are ignored (except for local_remote)")
				pass

			elif message['origin'] == 'TSO':
				if message['value_name'] == 'SPMAX': remote_spmax(ppc_master_obj)
				elif message['value_name'] == 'P_SP_TSO': tso_P_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'Q_SP_TSO': tso_Q_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'V_SP_TSO': tso_V_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'PF_SP_TSO': tso_PF_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'ENAP': remote_enap(ppc_master_obj, window_obj)
				elif message['value_name'] == '10': remote_10min(ppc_master_obj, window_obj)

			elif message['origin'] == 'FOSE':
				if message['value_name'] == 'SPMAX': remote_spmax(ppc_master_obj)
				elif message['value_name'] == 'P_SP_FOSE': fose_P_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'Q_SP_FOSE': fose_Q_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'V_SP_FOSE': fose_V_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'PF_SP_FOSE': fose_PF_setpoint(ppc_master_obj, float(message["value"]))
				elif message['value_name'] == 'ENAP': remote_enap(ppc_master_obj, window_obj)
				elif message['value_name'] == '10': remote_10min(ppc_master_obj, window_obj)
		
		# Iterate through slaves
		for i in range(ppc_master_obj.numberOfSlaves):
			label = 'Slave_' + str(i+1)
			if message['origin'] == label:
				if message['value_name'] == 'Total_Pmax_available': ppc_master_obj.slave_pmax[i] = float(message["value"])
				elif message['value_name'] == 'Total_Qmax_available': ppc_master_obj.slave_qmax[i] = float(message["value"])
				elif message['value_name'] == 'Total_Qmin_available': ppc_master_obj.slave_qmin[i] = float(message["value"])
		
		if message['origin'] == 'HV_Meter':
			if message['value_name'] == 'V1': ppc_master_obj.v_actual = float(message["value"])/ppc_master_obj.V_nom
			elif message['value_name'] == 'Vab': ppc_master_obj.vab_actual = float(message["value"])/ppc_master_obj.V_nom
			elif message['value_name'] == 'Vbc': ppc_master_obj.vbc_actual = float(message["value"])/ppc_master_obj.V_nom
			elif message['value_name'] == 'Vca': ppc_master_obj.vca_actual = float(message["value"])/ppc_master_obj.V_nom
			elif message['value_name'] == 'f': ppc_master_obj.f_actual = float(message["value"])
			elif message['value_name'] == 'Pa': ppc_master_obj.p_actual_hv = float(message["value"])/ppc_master_obj.S_nom
			elif message['value_name'] == 'Qa': ppc_master_obj.q_actual_hv = float(message["value"])/ppc_master_obj.S_nom
			elif message['value_name'] == 'S': ppc_master_obj.s_actual_hv = float(message["value"])/ppc_master_obj.S_nom
			elif message['value_name'] == 'main_switch_position': ppc_master_obj.main_switch_pos = int(message["value"])

