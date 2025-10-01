from sim_functions import *
from limit import *
import scipy.signal
from digitalfilter import *

# ---- LiveLFilter vs. SciPy’s lfilter -----------
# define lowpass filter with 2.5 Hz cutoff frequency
fs = 30  # sampling rate, Hz
b, a = scipy.signal.iirfilter(2, Wn=0.5, fs=fs, btype="low", ftype="butter")
p_filter = LiveLFilter(b, a)
q_filter = LiveLFilter(b, a)

# Internal setpoints
prev_p_in_sp = 0
prev_q_in_sp = 0
p_in_sp = 0
q_in_sp = 0

def simulatorCore(i, ppc_master_obj):
	global shutdown, prev_time
	global p_in_sp, q_in_sp, prev_p_in_sp, prev_q_in_sp

	# Check frequency and voltage ranges
	shutdown = operating_ranges(ppc_master_obj, window_obj)

	if ppc_master_obj.f_shutdown != 0:
		ppc_master_obj.operational_state = ppc_master_obj.f_shutdown
	elif ppc_master_obj.v_shutdown != 0:
		ppc_master_obj.operational_state = ppc_master_obj.v_shutdown
    
	# Select active power control strategy
	p_in_sp = F_control_sim(prev_p_in_sp, ppc_master_obj)
	q_in_sp = V_control_sim(ppc_master_obj)

	# limit control
	p_in_sp, q_in_sp = limit(p_in_sp, q_in_sp, ppc_master_obj)

	# Needed for the PID to follow along when not activated
	prev_p_in_sp = p_in_sp
	prev_q_in_sp = q_in_sp

	if ppc_master_obj.operational_state == 1:
		ppc_master_obj.p_in_sp = 0
		ppc_master_obj.q_in_sp = 0
	else:
		# update class variables
		ppc_master_obj.p_in_sp = p_in_sp
		ppc_master_obj.q_in_sp = q_in_sp

	# Single inverter emulator part
	p_actual = p_filter(p_in_sp)
	q_actual = q_filter(q_in_sp)
	# No grid model
	
	time.sleep(1)
	prev_time = now

