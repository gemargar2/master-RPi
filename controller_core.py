from distribution import *
from gradient_control import *
from F_control import *
from V_control import *
from limit import *
import time

# Internal setpoints
p_pid_flag = True
q_pid_flag = True

def populate_vectors(ppc_master_obj):
	# samples/timestamp	
	# ------ P plot -------
	# P remote setpoints
	ppc_master_obj.p_scada_sp.append(ppc_master_obj.local_P_sp)
	ppc_master_obj.p_tso_sp.append(ppc_master_obj.tso_P_sp)
	ppc_master_obj.p_fose_sp.append(ppc_master_obj.fose_P_sp)
	# P internal setpoints
	ppc_master_obj.p_in_sp_data.append(ppc_master_obj.p_in_sp)
	ppc_master_obj.p_grad_sp_data.append(ppc_master_obj.p_grad_sp)
	ppc_master_obj.p_pid_sp_data.append(ppc_master_obj.p_pid_sp)
	# P measurement
	ppc_master_obj.p_actual_data.append(ppc_master_obj.p_actual_hv)
		
	# F plot
	ppc_master_obj.f_data.append(ppc_master_obj.f_actual)
	ppc_master_obj.f_up.append(51)
	ppc_master_obj.f_dn.append(49)
	ppc_master_obj.f_up2.append(51.5)
	ppc_master_obj.f_dn2.append(47.5)
		
	# ------ Q plot -------
	# Q remote setpoints
	ppc_master_obj.q_scada_sp.append(ppc_master_obj.local_Q_sp)
	ppc_master_obj.q_tso_sp.append(ppc_master_obj.tso_Q_sp)
	ppc_master_obj.q_fose_sp.append(ppc_master_obj.fose_Q_sp)
	# Q internal setpoints
	ppc_master_obj.q_in_sp_data.append(ppc_master_obj.q_in_sp)
	ppc_master_obj.q_grad_sp_data.append(ppc_master_obj.q_grad_sp)
	ppc_master_obj.q_pid_sp_data.append(ppc_master_obj.q_pid_sp)
	# Q measurement
	ppc_master_obj.q_actual_data.append(ppc_master_obj.q_actual_hv)
		
	# V plots
	ppc_master_obj.vab_data.append(ppc_master_obj.vab_actual)
	ppc_master_obj.vbc_data.append(ppc_master_obj.vbc_actual)
	ppc_master_obj.vca_data.append(ppc_master_obj.vca_actual)
	ppc_master_obj.v_up.append(1.118)
	ppc_master_obj.v_dn.append(0.9)
	ppc_master_obj.v_up2.append(1.15)
	ppc_master_obj.v_dn2.append(0.85)

def controllerCore(window_obj, ppc_master_obj):
	global p_pid_flag, q_pid_flag
	
	# 1st task: Check frequency and voltage ranges
	# shutdown = operating_ranges(ppc_master_obj, window_obj)
	operating_ranges(ppc_master_obj, window_obj)
	
	# 2nd task: for remote level apply setpoint priority (lowest value)
	# ----- Comment out for testbench --------
	# ppc_master_obj.setpoint_priority()
	# ----- Comment out for testbench --------
	
	# 3rd task: Specify the setpoint AFTER the transient phenomenon (gradient control + PGS step response)
	if ppc_master_obj.operational_state == 1:
		ppc_master_obj.p_in_sp = 0
		ppc_master_obj.q_in_sp = 0
		ppc_master_obj.p_grad_sp = 0
		ppc_master_obj.q_grad_sp = 0
		ppc_master_obj.p_pid_sp = 0
		ppc_master_obj.q_pid_sp = 0
		ppc_master_obj.prev_p_grad_sp = 0
		ppc_master_obj.prev_q_grad_sp = 0
		ppc_master_obj.prev_p_pid_sp = 0
		ppc_master_obj.prev_q_pid_sp = 0
	else:
		if ppc_master_obj.lfsm_flag:
			if ppc_master_obj.lfsm_pref_flag:
				window_obj.ax1.set_title('Active power: LFSM-O/U')
				print("LFSM First time")
				ppc_master_obj.lfsm_pref = ppc_master_obj.p_actual_hv
				ppc_master_obj.lfsm_pref_flag = False
				ppc_master_obj.fsm_pref_flag = True
				print(f'LFSM Pref = {ppc_master_obj.lfsm_pref}')
			ppc_master_obj.p_in_sp = LFSM_VDE(ppc_master_obj.lfsm_pref, ppc_master_obj, window_obj)
		else:
			ppc_master_obj.lfsm_pref_flag = True
			# Select active power control strategy
			if ppc_master_obj.p_mode == 0:
				window_obj.ax1.set_title('Active power: P control')
				ppc_master_obj.p_in_sp = ppc_master_obj.p_ex_sp
				p_pid_flag = True
				ppc_master_obj.fsm_pref_flag = True
			elif ppc_master_obj.p_mode == 1:
				if ppc_master_obj.fsm_pref_flag:
					print("FSM First time")
					ppc_master_obj.fsm_pref = ppc_master_obj.p_actual_hv
					ppc_master_obj.fsm_pref_flag = False
					print(f'FSM Pref = {ppc_master_obj.fsm_pref}')
				window_obj.ax1.set_title('Active power: F control')
				# p_in_sp = F_Control(ppc_master_obj, window_obj)
				ppc_master_obj.p_in_sp = FSM_VDE(ppc_master_obj.fsm_pref, ppc_master_obj, window_obj)
				p_pid_flag = True
			elif ppc_master_obj.p_mode == 2: # P Open Loopl
				window_obj.ax1.set_title('Active power: P open loop')
				ppc_master_obj.p_in_sp = ppc_master_obj.p_ex_sp
				p_pid_flag = False
				ppc_master_obj.fsm_pref_flag = True
			elif ppc_master_obj.p_mode == 3: # MPPT
				window_obj.ax1.set_title('Active power: MPPT')
				ppc_master_obj.p_in_sp = ppc_master_obj.total_pmax/ppc_master_obj.S_nom
				p_pid_flag = False
				ppc_master_obj.fsm_pref_flag = True
	    
		# Select reactive power control strategy
		if ppc_master_obj.q_mode == 0:
			window_obj.ax3.set_title('Reactive power: Q control')
			ppc_master_obj.q_in_sp = ppc_master_obj.q_ex_sp
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 1:
			window_obj.ax3.set_title('Reactive power: Q(P)')
			ppc_master_obj.q_in_sp = QP_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 2:
			window_obj.ax3.set_title('Reactive power: V control')
			ppc_master_obj.q_in_sp = V_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 3:
			window_obj.ax3.set_title('Reactive power: PF control')
			ppc_master_obj.q_in_sp = PF_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 4:
			window_obj.ax3.set_title('Reactive power: Q open loop')
			ppc_master_obj.q_in_sp = ppc_master_obj.q_ex_sp
			q_pid_flag = False
		elif ppc_master_obj.q_mode == 5:
			window_obj.ax3.set_title('Reactive power: Q(U)')
			ppc_master_obj.q_in_sp = QU_VDE(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 6:
			window_obj.ax3.set_title('Reactive power: Q(U) with limit')
			ppc_master_obj.q_in_sp = V_Limit_VDE(ppc_master_obj)
			q_pid_flag = True
	    
		# Active [0,1] / Reactive power Q-P Q-V shape limit control
		ppc_master_obj.p_in_sp, ppc_master_obj.q_in_sp = limit(ppc_master_obj)
	
		# 4th task: Apply gradient control to restrict overshoot
		ppc_master_obj.p_grad_sp, ppc_master_obj.q_grad_sp = gradient_control(ppc_master_obj, ppc_master_obj.prev_p_grad_sp, ppc_master_obj.prev_q_grad_sp)
	
		# 5th task: Apply PI control to ensure that PGS reaches the desired setpoint
		# P PID
		# Check PID flag AND if active power measurement is near the final setpoint
		if p_pid_flag and abs(ppc_master_obj.p_in_sp-ppc_master_obj.p_actual_hv)<0.06:
			ppc_master_obj.p_pid_sp = P_control(ppc_master_obj.p_grad_sp, ppc_master_obj.prev_p_pid_sp, ppc_master_obj)
		else: ppc_master_obj.p_pid_sp = ppc_master_obj.p_grad_sp
		# Q PID
		if q_pid_flag: ppc_master_obj.q_pid_sp = Q_control(ppc_master_obj.q_grad_sp, ppc_master_obj.prev_q_pid_sp, ppc_master_obj)
		else: ppc_master_obj.q_pid_sp = ppc_master_obj.q_grad_sp
	
	
	# Needed for the PID to follow along when not activated
	ppc_master_obj.prev_p_grad_sp = ppc_master_obj.p_grad_sp
	ppc_master_obj.prev_q_grad_sp = ppc_master_obj.q_grad_sp
		
	# Needed for the PID to follow along when not activated
	ppc_master_obj.prev_p_pid_sp = ppc_master_obj.p_pid_sp
	ppc_master_obj.prev_q_pid_sp = ppc_master_obj.q_pid_sp
	
	# 6th task: recalculate slave contribution percentages to implement distribution
	recalc_contribution(ppc_master_obj, window_obj)
	recalc_pf(ppc_master_obj)
	populate_vectors(ppc_master_obj)
