import math

# --- PID controllers --------------------------------

def p_pid_controller(setpoint, pv, kp, ki, kd, previous_error, integral, dt):
	error = setpoint - pv
	integral += error * dt
	derivative = (error - previous_error) / dt
	control = kp * error + ki * integral + kd * derivative

	return control, error, integral

def q_pid_controller(setpoint, pv, kp, ki, kd, previous_error, integral, dt):
	error = setpoint - pv
	integral += error * dt
	derivative = (error - previous_error) / dt
	control = kp * error + ki * integral + kd * derivative
 
	return control, error, integral

# --- Gradient control -------------------------------

q_grad = 0

def gradient_control(ppc_master_obj, prev_p_sp, prev_q_sp):
	global q_grad

	# Active power gradient
	# Convert p.u/sec to p.u/sample = p.u/sampling_period = MW/(S_nom*sampling_period)
	if ppc_master_obj.p_mode == 3: # MPPT
		grad = ppc_master_obj.MPPT_grad/ppc_master_obj.sampling_rate
	elif ppc_master_obj.p_mode == 1: # F control
		grad = ppc_master_obj.F_grad/ppc_master_obj.sampling_rate
	else: # P Control or P Open Loop
		grad = ppc_master_obj.P_grad/ppc_master_obj.sampling_rate
	
	# Deadband: if active power remains less than 1 grad unit (= 0.33%/sec = 0.000165p.u/sample)
	# but your previous setpoint is greater or equal then stop ascending
	#if ppc_master_obj.p_actual_hv < 0.0001 and prev_p_sp > 0.0001:
	#	prev_p_sp = 0.0001
	#else: 
	if (ppc_master_obj.p_in_sp - prev_p_sp > grad): prev_p_sp += grad
	elif (prev_p_sp - ppc_master_obj.p_in_sp > grad): prev_p_sp -= grad
	else: prev_p_sp = ppc_master_obj.p_in_sp
	
	response_time = 5 # response time in seconds
	delta_q = ppc_master_obj.q_in_sp - ppc_master_obj.prev_q_in_sp
	# print(delta_q)
	if (abs(delta_q) > 0.01):
		q_grad = delta_q/(response_time*ppc_master_obj.sampling_rate)
		print(q_grad)
	
	if (abs(ppc_master_obj.q_in_sp - prev_q_sp) > abs(q_grad)): prev_q_sp += q_grad
	else: prev_q_sp = ppc_master_obj.q_in_sp
	# prev_q_sp = ppc_master_obj.q_in_sp

	return prev_p_sp, prev_q_sp

# --- Active power ---------------------------------

# PID aux variables
p_prev_error = 0
q_prev_error = 0
p_integral = 0
q_integral = 0

# P mode = 0
def P_control(p_grad_sp, prev_p_grad_sp, ppc_master_obj):
	global p_integral, p_prev_error
	# Parameters
	kp = ppc_master_obj.p_kp   # Proportional gain
	ki = ppc_master_obj.p_ki   # Integral gain
	kd = ppc_master_obj.p_kd   # Derivative gain
	dt = ppc_master_obj.p_dt   # 100 ms
	# Power control model
	p_control, p_error, p_integral = p_pid_controller(p_grad_sp, ppc_master_obj.p_actual_hv, kp, ki, kd, p_prev_error, p_integral, dt)
	p_pid_sp = prev_p_grad_sp + p_control * dt
	p_prev_error = p_error
	
	if p_pid_sp >= 1: p_pid_sp = 1
	if p_pid_sp <= 0: p_pid_sp = 0
	
	#if ((ppc_master_obj.p_actual_hv < 0.0001) and (p_pid_sp > 0.0001)): p_pid_sp = 0.0001

	return p_pid_sp

# --- Rective power ---------------------------------

# Q mode = 0
def Q_control(q_grad_sp, prev_q_grad_sp, ppc_master_obj):
	global q_integral, q_prev_error
	# Parameters
	kp = ppc_master_obj.q_kp   # Proportional gain
	ki = ppc_master_obj.q_ki   # Integral gain
	kd = ppc_master_obj.q_kd   # Derivative gain
	dt = ppc_master_obj.q_dt   # 100 ms
	# Power control model
	q_control, q_error, q_integral = q_pid_controller(q_grad_sp, ppc_master_obj.q_actual_hv, kp, ki, kd, q_prev_error, q_integral, dt)
	q_pid_sp = prev_q_grad_sp + q_control * dt
	q_prev_error = q_error
	
	if q_pid_sp >= 1: q_pid_sp = 1
	if q_pid_sp <= -1: q_pid_sp = -1
	
	#if ((ppc_master_obj.p_actual_hv < 0.0001) and (q_pid_sp > 0.0001)): q_pid_sp = 0.0001
	#if ((ppc_master_obj.p_actual_hv > -0.0001) and (q_pid_sp < -0.0001)): q_pid_sp = -0.0001

	return q_pid_sp

# Q mode = 1
def QP_control(ppc_master_obj):
	index = 0
	for i in range(ppc_master_obj.numOfPoints-1):
		if (ppc_master_obj.p_in_sp < float(ppc_master_obj.P_points[i+1])) and (ppc_master_obj.p_in_sp >= float(ppc_master_obj.P_points[i])):
			index = i
			break
	#print(index)
	q_in_sp = (ppc_master_obj.p_in_sp - float(ppc_master_obj.P_points[index]))*ppc_master_obj.m[i] + float(ppc_master_obj.Q_points[i])
	return q_in_sp

# Q mode = 3
def PF_control(ppc_master_obj):
	q_in_sp = ppc_master_obj.p_actual_hv * math.tan(math.acos(ppc_master_obj.pf_ex_sp))
	return q_in_sp

# Hello sunshine
def recalc_pf(ppc_master_obj):
	if ppc_master_obj.p_actual_hv == 0:
		ppc_master_obj.pf_actual = 1
	else:
		ppc_master_obj.pf_actual = math.cos(math.atan(ppc_master_obj.q_actual_hv/ppc_master_obj.p_actual_hv))
		if ppc_master_obj.q_actual_hv < 0: ppc_master_obj.pf_actual = -ppc_master_obj.pf_actual
