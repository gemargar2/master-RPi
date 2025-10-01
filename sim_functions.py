from ramp_control import *

printMessages = True

f_ref = 50.0 # Frequency setpoint is always 50.0 Hz
dt = 0.1

# F control submode
# 0 = FSM
# 1 = deadband
# 2 = constant setpoint
# 3 = LFSM_O
# 4 = LFSM_U
f_mode = 0
f_integral = 0
f_prev_error = 0

def F_ramp_control(ppc_master_obj, p_in_sp, prev_p_in_sp):
	grad = ppc_master_obj.F_grad

	if (p_in_sp - prev_p_in_sp > grad):
		res = prev_p_in_sp + grad
	elif (prev_p_in_sp - p_in_sp > grad):
		res = prev_p_in_sp - grad
	else:
		res = p_in_sp

	return res

# --- F control -------------------------------------

def LFSM_U_sim(p_ref, ppc_master_obj):
	s2 = ppc_master_obj.s_LFSM_U # Droop default value 5%
	f_1 = 49.8 # LFSM-U frequency threshold default 49.8Hz
	delta_P = (f_1-ppc_master_obj.f_actual)/(f_ref*s2) # positive for f_actual<f_1 (underfrequency)
	p_in_sp = (p_ref + 0.19/(ppc_master_obj.s_FSM*f_ref)) + delta_P

	return p_in_sp

def LFSM_O_sim(p_ref, ppc_master_obj):
	s2 = ppc_master_obj.s_LFSM_O # Droop default value 5%
	f_1 = 50.2 # LFSM-O frequency threshold default 50.2Hz
	delta_P = (f_1-ppc_master_obj.f_actual)/(f_ref*s2) # negative for f_actual>f_1 (overfrequency)
	p_in_sp = (p_ref - 0.19/(ppc_master_obj.s_FSM*f_ref)) + delta_P

	return p_in_sp

def FSM_sim(p_ref, ppc_master_obj):
	s = ppc_master_obj.s_FSM # Droop adjustable between 2-12%, default value 5%
	delta_P = (f_ref-ppc_master_obj.f_actual)/(f_ref*s) # positive for f_actual<f_ref (underfrequency), negative for f_actual>f_ref (overfrequency)
	p_in_sp = p_ref + delta_P

	return p_in_sp

def F_control_sim(prev_p_in_sp, ppc_master_obj):
	global f_mode
	p_ref = ppc_master_obj.PF_p
	# ---------------
	# Under frequency
	# ---------------
	# While frequency remains below 50.0Hz the PGM should be capable of continuously
	# increasing its active power generation under a steady active power – frequency droop (s1)
	if (49.8 <= ppc_master_obj.f_actual < 49.99) and (ppc_master_obj.p_actual_hv < 1.0):
		if printMessages and f_mode != 0:
			print("FSM underfrequency")
			f_mode = 0
		p_in_sp = FSM(p_ref, ppc_master_obj)
	# This increase should last until either system frequency restores at a value within a -10mHz dead band
	# around 50.0Hz or the PGM reaches its maximum capacity (Pmax).
	elif (49.99 <= ppc_master_obj.f_actual < 50.0):
		if printMessages and f_mode != 1:
			print("Deadband")
			f_mode = 1
		p_in_sp = p_ref
	# Upon reaching Pmax the PGM shall be capable of continuing operation at constant power control mode. 
	elif ppc_master_obj.p_actual_hv >= 1.0:
		window_obj.ax8.set_title('P(f): Constant setpoint P_max')
		if printMessages and f_mode != 2:
			print("Constant setpoint P_max")
			f_mode = 2
		p_in_sp = 1.0
	# In case that system frequency decreases further below 49.8Hz and the PGM has not reached its maximum capacity,
	# the PGM should operate under the LFSM-U.
	elif (ppc_master_obj.f_actual < 49.8) and (ppc_master_obj.p_actual_hv < 1.0):
		if printMessages and f_mode != 3:
			print("LFSM_U")
			f_mode = 3
		p_in_sp = LFSM_U(p_ref, ppc_master_obj)
	# --------------
	# Over frequency
	# --------------
	# While frequency remains above 50.0Hz the PGM should be capable of continuously
	# decreasing its active power generation under a steady active power – frequency droop (s1).
	elif (50.01 <= ppc_master_obj.f_actual < 50.2) and (ppc_master_obj.p_actual_hv > 0.0):
		if printMessages and f_mode != 0:
			print("FSM overfrequency")
			f_mode = 0
		p_in_sp = FSM(p_ref, ppc_master_obj)
	# This increase should last until either system frequency reduces at a value within a +10mHz dead band
	# around 50.0Hz or the PGM reaches its active power minimum regulating level.
	elif (50.0 <= ppc_master_obj.f_actual <= 50.01):
		if printMessages and f_mode != 1:
			print("Deadband")
			f_mode = 1
		p_in_sp = p_ref
	# Upon reaching minimum regulating level, the PGM shall be capable of continuing operation at constant power control mode. 
	elif ppc_master_obj.p_actual_hv <= 0.0:
		if printMessages and f_mode != 2:
			print("Constant setpoint P_min")
			f_mode = 2
		p_in_sp = 0.0
	# In case that system frequency increases further above 50.2Hz and the PGM has not reached its minimum regulating level,
	# the PGM should operate under the LFSM-O
	elif (ppc_master_obj.f_actual > 50.2) and (ppc_master_obj.p_actual_hv > 0.0):
		if printMessages and f_mode != 4:
			print("LFSM_O")
			f_mode = 4
		p_in_sp = LFSM_O(p_ref, ppc_master_obj)
	# Default value to avoid error "p_in_sp referenced before assignment"
	else:
		p_in_sp = 0.5

	# Ramp BEFORE PID = avoid integral error overflow
	# Ramp AFTER PID = avoid output changing to steeply
	p_in_sp1 = F_ramp_control(ppc_master_obj, p_in_sp, prev_p_in_sp)

	return p_in_sp1

# Q mode = 2
def V_control_sim(ppc_master_obj):
    q_ref = 0 # ppc_master_obj.q_ex_sp
    v_actual = ppc_master_obj.v_actual
    
    if ppc_master_obj.local_remote == 0: v_sp = ppc_master_obj.local_V_sp # setpoint voltage
    else: v_sp = ppc_master_obj.remote_V_sp # setpoint voltage

    slope = ppc_master_obj.slope_sp # Droop adjustable between 2-12%, default value 5%
    db = ppc_master_obj.V_deadband_sp # voltage deadband
    m = 1/slope # gradient 7<m<24

    if (v_actual < v_sp - db):
        if printMessages:
            print(f'{v_actual} < {v_sp - db}')
            print("Under voltage")
        delta_V = (v_sp - db) - v_actual
        delta_Q = delta_V * m
        q_in_sp = q_ref + delta_Q
    elif (v_actual > v_sp + db):
        if printMessages:
            print(f'{v_actual} > {v_sp + db}')
            print("Over voltage")
        delta_V = v_actual - (v_sp + db)
        delta_Q = delta_V * m
        q_in_sp = q_ref - delta_Q
    else:
        q_in_sp = q_ref

    return q_in_sp
    