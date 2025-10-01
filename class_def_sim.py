import zmq
import time
import threading
from numpy import zeros
from F_control import *

class PPC_master_class_sim:
	def __init__(self, json_obj):
		# --- Configuration ----------------------------
		self.configdata = json_obj
		# Nominal ratings
		self.S_nom = float(self.configdata["master"]["nominal_power"]) # Nominal apparent power in MVA
		self.P_nom = float(self.configdata["master"]["nominal_power"]) # Nominal active power in MW
		self.V_nom = float(self.configdata["master"]["nominal_voltage"]) # Nominal voltage in kV
		# --- Signals ----------------------------
		# Mode of operation for active and reactive control
		self.p_mode = 2 # 0 = P control (PID) / 1 = F control (FSM) / 2 = P Open Loop / 3 = MPPT control
		self.q_mode = 4 # 0 = Q control (PID) / 1 = Q(P) control / 2 = V control / 3 = PF control / 4 = Q Open Loop / 5 = Q(U) / 6 = Q(U) with limit	
		# Status
		self.f_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.v_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		# Local setpoints (SCADA)
		self.local_P_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_P_sp"]/self.S_nom
		self.local_Q_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_Q_sp"]/self.S_nom
		self.local_PF_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_PF_sp"]
		self.local_V_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_V_sp"]/self.V_nom
		# Gradient values (setpoint rate of change MW/sec or p.u/sample)
		self.P_grad = self.configdata["PPC_parameters"]["power_gradients"]["P_grad"]/self.S_nom # p.u/sample
		self.F_grad = self.configdata["PPC_parameters"]["power_gradients"]["F_grad"]/self.S_nom # p.u/sample
		self.MPPT_grad = self.configdata["PPC_parameters"]["power_gradients"]["MPPT_grad"]/self.S_nom # p.u/sample
		# P control PID parameters
		self.p_kp = self.configdata["PPC_parameters"]["P_PID_parameters"]["p_kp"] # Proportional gain
		self.p_ki = self.configdata["PPC_parameters"]["P_PID_parameters"]["p_ki"] # Integral gain
		self.p_kd = self.configdata["PPC_parameters"]["P_PID_parameters"]["p_kd"] # Derivative gain
		self.p_dt = self.configdata["PPC_parameters"]["P_PID_parameters"]["p_dt"] # Integration/Derivation time constant
		# P control PID parameters
		self.q_kp = self.configdata["PPC_parameters"]["Q_PID_parameters"]["q_kp"] # Proportional gain
		self.q_ki = self.configdata["PPC_parameters"]["Q_PID_parameters"]["q_ki"] # Integral gain
		self.q_kd = self.configdata["PPC_parameters"]["Q_PID_parameters"]["q_kd"] # Derivative gain
		self.q_dt = self.configdata["PPC_parameters"]["Q_PID_parameters"]["q_dt"] # Integration/Derivation time constant
		# External setpoints (init with local values)
		self.p_ex_sp = self.local_P_sp
		# print(self.p_ex_sp)
		self.q_ex_sp = self.local_Q_sp
		self.pf_ex_sp = self.local_PF_sp
		# Setpoints with gradient
		self.p_grad_sp = 0
		self.q_grad_sp = 0
		# Setpoints with gradient
		self.p_in_sp = 0
		self.q_in_sp = 0
		# HV meter
		self.p_actual_hv = 0
		self.q_actual_hv = 0
		self.f_actual = 50
		self.v_actual = 1
		# MV meter main
		self.p_actual_mv = 0
		self.q_actual_mv = 0
		# Control curves
		# P(f)
		self.s_FSM = self.configdata["PPC_parameters"]["P(f)_curve"]["s_FSM"]
		self.s_LFSM_O = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_O"]
		self.s_LFSM_U = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_U"]
		self.PF_p = self.configdata["PPC_parameters"]["P(f)_curve"]["p_ref"]
		# V control
		self.slope_sp = self.configdata["PPC_parameters"]["V_control_curve"]["slope_sp"]
		self.V_deadband_sp = self.configdata["PPC_parameters"]["V_control_curve"]["V_deadband_sp"]
		# Q(U)
		self.QU_db = self.configdata["PPC_parameters"]["Q(U)_curve"]["deadband"]
		self.QU_s = self.configdata["PPC_parameters"]["Q(U)_curve"]["slope"]
		self.QU_v = self.configdata["PPC_parameters"]["Q(U)_curve"]["v_ref"]
		# Q(U) w/Limit
		self.numOfPoints2 = 4 # by default
		self.U_points = self.configdata["PPC_parameters"]["Q(U)_Limit_curve"]["U_values"]
		self.Q_points2 = self.configdata["PPC_parameters"]["Q(U)_Limit_curve"]["Q_values"]
		self.QU_q = self.configdata["PPC_parameters"]["Q(U)_Limit_curve"]["q_ref"]
		self.P1 = [float(self.U_points[0]), float(self.Q_points2[0])]
		self.P2 = [float(self.U_points[1]), float(self.Q_points2[1])]
		self.P3 = [float(self.U_points[2]), float(self.Q_points2[2])]
		self.P4 = [float(self.U_points[3]), float(self.Q_points2[3])]
		self.ma = 0
		self.mb = 0
		self.dba = 0
		self.dbb = 0
		self.V_Limit_VDE_init(self.QU_q)

	def V_Limit_VDE_init(self, q_ref):
		# Slopes are not affected by voltage setpoint
		self.ma = (self.P2[1] - self.P1[1]) / (self.P2[0] - self.P1[0])
		self.mb = (self.P4[1] - self.P3[1]) / (self.P4[0] - self.P3[0])

		# Deadband limits are affected by voltage setpoint
		self.dba = self.P2[0] + q_ref / self.ma
		self.dbb = self.P3[0] + q_ref / self.mb

			
