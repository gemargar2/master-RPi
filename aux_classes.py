class setpoints():
    def __init__(self):
        # Local setpoints (SCADA)
        self.P_sp = 20
        self.Q_sp = 0
        self.PF_sp = 1
        self.sp = 1

class local_setpoints(setpoints):
    pass

class tso_setpoints(setpoints):
    pass

class fose_setpoints(setpoints):
    pass