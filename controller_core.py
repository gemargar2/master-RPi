from distribution import *
from F_control import *
from V_control import *
from limit import *
import time

dt = 0.1 # 100ms
time_interval = 1000 * dt # 100 miliseconds
prev_time = time.time()

# Internal setpoints
prev_p_in_sp = 0
prev_q_in_sp = 0
p_in_sp = 0
q_in_sp = 0

def controllerCore(i, window_obj, ppc_master_obj):
	global shutdown, prev_time
	global p_in_sp, q_in_sp, prev_p_in_sp, prev_q_in_sp

	now = time.time()
	time_elapsed = now - prev_time
	# print(time_elapsed)
	
	# 1st task: Check frequency and voltage ranges
	# shutdown = operating_ranges(ppc_master_obj, window_obj)
	operating_ranges(ppc_master_obj, window_obj)
	
	# 2nd task: for remote level apply setpoint priority (lowest value)
	ppc_master_obj.setpoint_priority()

	# 3rd task: apply gradient BEFORE feeding the PIDs to avoid integral error adding up
	p_grad_sp, q_grad_sp = ramp_rate(ppc_master_obj)
	
	if ppc_master_obj.operational_state == 1:
		p_in_sp = 0
		q_in_sp = 0
	else:
		# Select active power control strategy
		if ppc_master_obj.p_mode == 0:
			window_obj.ax1.set_title('Active power: P control')
			p_in_sp = P_control(p_grad_sp, prev_p_in_sp, ppc_master_obj)
		elif ppc_master_obj.p_mode == 1:
			window_obj.ax1.set_title('Active power: F control')
			p_in_sp = F_control(prev_p_in_sp, ppc_master_obj, window_obj)
		elif ppc_master_obj.p_mode == 2: # P Open Loop
			window_obj.ax1.set_title('Active power: P open loop')
			p_in_sp = p_grad_sp # P Open Loop = Just pass the external setpoint
		elif ppc_master_obj.p_mode == 3: # P Open Loop
			window_obj.ax1.set_title('Active power: MPPT')
			p_in_sp = p_grad_sp # P Open Loop = Just pass the external setpoint
	    
		# Select reactive power control strategy
		if ppc_master_obj.q_mode == 0:
			window_obj.ax3.set_title('Reactive power: Q control')
			q_in_sp = Q_control(q_grad_sp, prev_q_in_sp, ppc_master_obj)
		elif ppc_master_obj.q_mode == 1:
			window_obj.ax3.set_title('Reactive power: Q(P)')
			q_in_sp = QP_control(ppc_master_obj)
		elif ppc_master_obj.q_mode == 2:
			window_obj.ax3.set_title('Reactive power: V control')
			q_in_sp = V_control(ppc_master_obj)
		elif ppc_master_obj.q_mode == 3:
			window_obj.ax3.set_title('Reactive power: PF control')
			q_in_sp = PF_control(ppc_master_obj)
		elif ppc_master_obj.q_mode == 4:
			window_obj.ax3.set_title('Reactive power: Q open loop')
			q_in_sp = q_grad_sp # Q Open Loop = Just pass the external setpoint
		elif ppc_master_obj.q_mode == 5:
			window_obj.ax3.set_title('Reactive power: Q(U)')
			q_in_sp = QU_VDE(ppc_master_obj)
		elif ppc_master_obj.q_mode == 6:
			window_obj.ax3.set_title('Reactive power: Q(U) with limit')
			q_in_sp = V_Limit_VDE(ppc_master_obj)
	    
		# Reacive power Q-P Q-V shape limit control
		p_in_sp, q_in_sp = limit(p_in_sp, q_in_sp, ppc_master_obj)
	
	# Needed for the PID to follow along when not activated
	prev_p_in_sp = p_in_sp
	prev_q_in_sp = q_in_sp
	# ???
	ppc_master_obj.p_in_sp = p_in_sp
	ppc_master_obj.q_in_sp = q_in_sp
	# 4th task: recalculate slave contribution percentages
	recalc_contribution(ppc_master_obj, window_obj)

	# End of cycle - reset timer
	prev_time = now

