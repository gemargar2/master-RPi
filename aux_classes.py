from collections import deque

class setpoints():
    def __init__(self):
        self.P_sp = 20
        self.Q_sp = 0
        self.PF_sp = 1
        self.V_sp = 1

class pid_params():
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.dt = 0

class basic_struct():
    def __init__(self):
        self.input = 0
        self.output = 0
        self.prev_state = 0
    
    def zero(self):
        self.input = 0
        self.output = 0
        self.prev_state = 0

class basic_submod():
    def __init__(self):
        self.p = basic_struct()
        self.q = basic_struct()
    
    def zero(self):
        self.p.zero()
        self.q.zero()

class HV_meter_class():
    def __init__(self):
        # Power
        self.p_actual = 0 # Active
        self.q_actual = 0 # Reactive
        self.s_actual = 0 # Apparent
        # Frequency
        self.f_actual = 50
        # Voltage
        self.vab_actual = 1 # Phase a to phase b
        self.vbc_actual = 1 # Phase b to phase c
        self.vca_actual = 1 # Phase c to phase a
        self.v_actual = 1 # Positive sequence
        # Power factor
        self.pf_actual = 1
		# Main switch position
        self.main_switch_pos = 1 # 0 = Open / 1 = Closed

sampling_rate = 10 # 20Hz
time_window = 30 # 30 seconds
smax = time_window*sampling_rate # samples

class plot_vectors():
    def __init__(self):
        # Samples/timestamps
        self.x_data = deque([], maxlen=smax)
        # P remote setpoints
        self.p_scada_sp = deque([], maxlen=smax)
        self.p_tso_sp = deque([], maxlen=smax)
        self.p_fose_sp = deque([], maxlen=smax)
        # P internal setpoints
        self.p_in_sp_data = deque([], maxlen=smax)
        self.p_grad_sp_data = deque([], maxlen=smax)
        self.p_pid_sp_data = deque([], maxlen=smax)
        # P measurement
        self.p_actual_data = deque([], maxlen=smax)
        # F setpoint
        self.f_data = deque([], maxlen=smax)
        self.f_up = deque([], maxlen=smax)
        self.f_dn = deque([], maxlen=smax)
        self.f_up2 = deque([], maxlen=smax)
        self.f_dn2 = deque([], maxlen=smax)
        # Q remote setpoints
        self.q_scada_sp = deque([], maxlen=smax)
        self.q_tso_sp = deque([], maxlen=smax)
        self.q_fose_sp = deque([], maxlen=smax)
        # Q internal setpoints
        self.q_in_sp_data = deque([], maxlen=smax)
        self.q_grad_sp_data = deque([], maxlen=smax)
        self.q_pid_sp_data = deque([], maxlen=smax)
        # Q measurement
        self.q_actual_data = deque([], maxlen=smax)
        # V setpoint
        self.vab_data = deque([], maxlen=smax)
        self.vbc_data = deque([], maxlen=smax)
        self.vca_data = deque([], maxlen=smax)
        self.v_up = deque([], maxlen=smax)
        self.v_dn = deque([], maxlen=smax)
        self.v_up2 = deque([], maxlen=smax)
        self.v_dn2 = deque([], maxlen=smax)