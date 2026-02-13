
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

# --- F control VDE -------------------------------------

def LFSM_VDE(p_ref, ppc_master_obj):
	if ppc_master_obj.hv_meter.f_actual > 50.2:
		f_1 = 50.2 # LFSM-O frequency threshold default 50.2Hz
		delta_f = f_1-ppc_master_obj.hv_meter.f_actual # positive for f_actual<f_1 (underfrequency)
		delta_P = delta_f*0.4*p_ref # For overfrequency it is delta_P/delta_f = 40% * Pref/Hz where Pref = Pmom (instantaneous)
	elif ppc_master_obj.hv_meter.f_actual < 49.8:
		f_1 = 49.8 # LFSM-U frequency threshold default 49.8Hz
		delta_f = f_1-ppc_master_obj.hv_meter.f_actual # positive for f_actual<f_1 (underfrequency)
		delta_P = delta_f*0.4 # For overfrequency it is delta_P/delta_f = 40% * Pref/Hz where Pref = PrE (maximum rated)

	print(f'delta_P = {delta_P}')
	p_in_sp = p_ref + delta_P

	return p_in_sp

def FSM_VDE(p_ref, ppc_master_obj):
	s = ppc_master_obj.s_FSM # Droop adjustable between 2-12%, default value 5%
	if ppc_master_obj.hv_meter.f_actual > 50.01:
		delta_P = (50.01 - ppc_master_obj.hv_meter.f_actual)/(50*s) # negative for f_actual>f_ref (overfrequency)
	elif ppc_master_obj.hv_meter.f_actual < 49.99:
		delta_P = (49.99 - ppc_master_obj.hv_meter.f_actual)/(50*s) # positive for f_actual<f_ref (underfrequency)
	else:
		delta_P = 0
	
	p_in_sp = p_ref + delta_P
	
	#print(f's = {s}, delta_P = {delta_P}')
	#print(f'P({ppc_master_obj.f_actual}) = {p_in_sp}')

	return p_in_sp