from distribution import *
from gradient_control import *
from F_control import *
from V_control import *
from limit import *
import time

# Internal setpoints
prev_p_pid_sp = 0
prev_q_pid_sp = 0
p_in_sp = 0
q_in_sp = 0
p_pid_flag = True
q_pid_flag = True

def controllerCore(i, window_obj, ppc_master_obj):
	global p_in_sp, q_in_sp, prev_p_pid_sp, prev_q_pid_sp, p_pid_flag, q_pid_flag
	
	# 1st task: Check frequency and voltage ranges
	# shutdown = operating_ranges(ppc_master_obj, window_obj)
	operating_ranges(ppc_master_obj, window_obj)
	
	# 2nd task: for remote level apply setpoint priority (lowest value)
	ppc_master_obj.setpoint_priority()

	# 3rd task: apply gradient BEFORE feeding the PIDs to avoid integral error adding up
	# p_grad_sp, q_grad_sp = ramp_rate(ppc_master_obj)
	
	# 3rd task: Specify the setpoint AFTER the transient phenomenon (gradient control + PGS step response)
	if ppc_master_obj.operational_state == 1:
		p_in_sp = 0
		q_in_sp = 0
	else:
		# Select active power control strategy
		if ppc_master_obj.p_mode == 0:
			window_obj.ax1.set_title('Active power: P control')
			p_in_sp = ppc_master_obj.p_ex_sp
			p_pid_flag = True
		elif ppc_master_obj.p_mode == 1:
			window_obj.ax1.set_title('Active power: F control')
			p_in_sp = F_control(ppc_master_obj, window_obj)
			p_pid_flag = True
		elif ppc_master_obj.p_mode == 2: # P Open Loop
			window_obj.ax1.set_title('Active power: P open loop')
			p_in_sp = ppc_master_obj.p_ex_sp
			p_pid_flag = False
		elif ppc_master_obj.p_mode == 3: # MPPT
			window_obj.ax1.set_title('Active power: MPPT')
			p_in_sp = ppc_master_obj.total_pmax/ppc_master_obj.S_nom
			p_pid_flag = False
	    
		# Select reactive power control strategy
		if ppc_master_obj.q_mode == 0:
			window_obj.ax3.set_title('Reactive power: Q control')
			q_in_sp = ppc_master_obj.q_ex_sp
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 1:
			window_obj.ax3.set_title('Reactive power: Q(P)')
			q_in_sp = QP_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 2:
			window_obj.ax3.set_title('Reactive power: V control')
			q_in_sp = V_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 3:
			window_obj.ax3.set_title('Reactive power: PF control')
			q_in_sp = PF_control(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 4:
			window_obj.ax3.set_title('Reactive power: Q open loop')
			q_in_sp = ppc_master_obj.q_ex_sp
			q_pid_flag = False
		elif ppc_master_obj.q_mode == 5:
			window_obj.ax3.set_title('Reactive power: Q(U)')
			q_in_sp = QU_VDE(ppc_master_obj)
			q_pid_flag = True
		elif ppc_master_obj.q_mode == 6:
			window_obj.ax3.set_title('Reactive power: Q(U) with limit')
			q_in_sp = V_Limit_VDE(ppc_master_obj)
			q_pid_flag = True
	    
		# Active [0,1] / Reactive power Q-P Q-V shape limit control
		p_in_sp, q_in_sp = limit(p_in_sp, q_in_sp, ppc_master_obj)
	
	# 4th task: Apply gradient control to restrict overshoot
	p_grad_sp, q_grad_sp = gradient_control(ppc_master_obj, p_in_sp, q_in_sp)
	
	# 5th task: Apply PI control to ensure that PGS reaches the desired setpoint
	# P PID
	if p_pid_flag: p_pid_sp = P_control(p_grad_sp, prev_p_pid_sp, ppc_master_obj)
	else: p_pid_sp = p_grad_sp
	# Q PID
	if q_pid_flag: q_pid_sp = Q_control(q_grad_sp, prev_q_pid_sp, ppc_master_obj)
	else: q_pid_sp = q_grad_sp
	
	# Needed for the PID to follow along when not activated
	prev_p_pid_sp = p_pid_sp
	prev_q_pid_sp = q_pid_sp
	# ???
	ppc_master_obj.p_in_sp = p_in_sp
	ppc_master_obj.q_in_sp = q_in_sp
	
	ppc_master_obj.p_grad_sp = p_grad_sp
	ppc_master_obj.q_grad_sp = q_grad_sp
	
	ppc_master_obj.p_pid_sp = p_pid_sp
	ppc_master_obj.q_pid_sp = q_pid_sp
	
	# 6th task: recalculate slave contribution percentages to implement distribution
	recalc_contribution(ppc_master_obj, window_obj)

