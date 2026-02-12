class setpoints():
    def __init__(self):
        # Local setpoints (SCADA)
        self.P_sp = 20
        self.Q_sp = 0
        self.PF_sp = 1
        self.V_sp = 1

class pid_params():
    def __init__(self):
        # Local setpoints (SCADA)
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.dt = 0