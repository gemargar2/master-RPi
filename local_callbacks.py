import json

# Local setpoints

def local_P_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_P_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)

def local_Q_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_Q_sp = var/ppc_master_obj.S_nom # store as per-unit
	# Update plots
	window_obj.plot_QU_limit_curve(ppc_master_obj)

def local_PF_setpoint(ppc_master_obj, var):
	ppc_master_obj.local_PF_sp = var

def local_V_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.local_V_sp = var/ppc_master_obj.V_nom
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)

# Universal setpoints

def local_s_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_sp = var/100
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)

def local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_O = var/100
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)

def local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.s_LFSM_U = var/100
	# Update plots
	window_obj.plot_PF_curve(ppc_master_obj)

def local_slope_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.slope_sp = var/100
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)

def local_V_deadband_setpoint(ppc_master_obj, window_obj, var):
	# Update ppc_master_obj variable
	ppc_master_obj.V_deadband_sp = var/100
	# Update plots
	window_obj.plot_QU_curve(ppc_master_obj)

# Gradients

def local_P_gradient_setpoint(ppc_master_obj, var):
	ppc_master_obj.P_grad = var/ppc_master_obj.S_nom

def local_F_gradient_setpoint(ppc_master_obj, var):
	ppc_master_obj.F_grad = var/ppc_master_obj.S_nom

def local_MPPT_gradient_setpoint(ppc_master_obj, var):
	ppc_master_obj.MPPT_grad = var/ppc_master_obj.S_nom

