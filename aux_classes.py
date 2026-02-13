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

class basic_submod():
    def __init__(self):
        self.p = basic_struct()
        self.q = basic_struct()

class HV_meter_class():
    def __init__(self):
        self.p_actual = 0
        self.q_actual = 0
        self.s_actual = 0
        self.f_actual = 50
        self.vab_actual = 1
        self.vbc_actual = 1
        self.vca_actual = 1
        self.v_actual = 1
        self.pf_actual = 1
		# Main switch position
        self.main_switch_pos = 1 # 0 = Open / 1 = Closed