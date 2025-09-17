import zmq
import time
import threading
from numpy import zeros
from F_control import *

class PPC_master_class:
	def __init__(self, json_obj, json_obj2):
		# --- Configuration ----------------------------
		# Store setpoints in m
		self.memory = json_obj
		self.configdata = json_obj2
		# General description
		self.name = self.configdata["device"]["name"]
		self.description = self.configdata["device"]["description"]
		self.type = self.configdata["device"]["plant_type"]
		self.surface_type = self.configdata["device"]["surface_type"]
		self.surface_tilt = self.configdata["device"]["surface_tilt"]
		self.surface_azimuth = self.configdata["device"]["surface_azimuth"]
		self.solar_zenith = self.configdata["device"]["solar_zenith"]
		self.solar_azimuth = self.configdata["device"]["solar_azimuth"]
		self.temp_coefficient = self.configdata["device"]["temp_coefficient_of_power"]
		# Nominal ratings
		self.S_nom = float(self.configdata["device"]["nominal_power"]) # Nominal apparent power in MVA
		self.P_nom = float(self.configdata["device"]["nominal_power"]) # Nominal active power in MW
		self.V_nom = float(self.configdata["device"]["nominal_voltage"]) # Nominal voltage in kV
		# Slave PPCs management
		self.slaves_data = self.configdata["device"]["slaves"]
		self.numberOfSlaves = len(self.slaves_data) # number of slaves
		self.slaves_Pinst = [] # nominal power of slaves
		self.slave_id = []
		# Slaves availability
		self.slave_pmax = zeros(self.numberOfSlaves) # Pmax available
		self.slave_qmax = zeros(self.numberOfSlaves) # Qmax available
		self.slave_qmin = zeros(self.numberOfSlaves) # Qmin available
		# Contribution percentages
		self.pi_per = zeros(self.numberOfSlaves) # percentage of contribution to the injected active power
		self.qi_per = zeros(self.numberOfSlaves) # percentage of contribution to the injected reactive power
		self.qa_per = zeros(self.numberOfSlaves) # percentage of contribution to the absorbed reactive power
		# Slave internal setpoints
		self.slave_p_sp = zeros(self.numberOfSlaves)
		self.slave_q_sp = zeros(self.numberOfSlaves)
		# Summary
		self.total_pmax = 0 # MW
		self.total_qmax = 0 # MVAR
		self.total_qmin = 0 # MVAR
		self.connect_to_slaves()
		# --- Establish connection for transmission --------------
		self.context_tx = zmq.Context()
		self.socket_tx = self.context_tx.socket(zmq.PUSH)
		self.socket_tx.bind("ipc:///tmp/zmqsub")
		# --- Establish connection for reception --------------
		self.context_rx = zmq.Context()
		self.socket_rx = self.context_rx.socket(zmq.PULL)
		self.socket_rx.connect("ipc:///tmp/zmqpub")
		time.sleep(5)
		# --- Signals ----------------------------
		# Local = SCADA / Remote = TSO
		self.local_remote = 0 # 0 = Local / 1 = Remote
		# Mode of operation for active and reactive control
		self.p_mode = 2 # 0 = P control (PID) / 1 = F control (FSM) / 2 = P Open Loop / 3 = MPPT control
		self.q_mode = 4 # 0 = Q control (PID) / 1 = Q(P) control / 2 = V control / 3 = PF control / 4 = Q Open Loop / 5 = Q(U) / 6 = Q(U) with limit
		# Per unit values
		self.max_P_cap = 1 # Max active power capability (meteo are ignored)
		self.max_Q_cap = 0.2 # Max reactive power capability
		self.min_Q_cap = -0.35 # Max reactive power capability
		# Status
		self.operational_state = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.f_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.v_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.auto_start_state = 0 # 0 = OFF / 1 = ON
		self.main_switch_pos = 1 # 0 = Open / 1 = Closed
		# Local setpoints (SCADA)
		self.local_P_sp = float(json_obj["local_P_sp"])/self.S_nom
		self.local_Q_sp = float(json_obj["local_Q_sp"])/self.S_nom
		self.local_PF_sp = float(json_obj["local_PF_sp"])
		self.local_V_sp = float(json_obj["local_V_sp"])/self.V_nom
		# Remote setpoints (TSO)
		self.remote_P_sp = float(json_obj["remote_P_sp"])/self.S_nom
		self.remote_Q_sp = float(json_obj["remote_Q_sp"])/self.S_nom
		self.remote_PF_sp = float(json_obj["remote_PF_sp"])
		self.remote_V_sp = float(json_obj["remote_V_sp"])/self.V_nom
		# Network Operator setpoints (TSO)
		self.tso_P_sp = float(json_obj["remote_P_sp"])/self.S_nom # Minimum p.u
		self.tso_Q_sp = float(json_obj["remote_Q_sp"])/self.S_nom # Minimum p.u
		# 3rd party setpoints (FOSE)
		self.fose_P_sp = 1 # Maximum p.u
		self.fose_Q_sp = 0.2 # Maximum p.u
		# Universal setpoints (configured by SCADA)
		self.s_sp = float(json_obj["s_sp"])
		self.s_LFSM_O = float(json_obj["s_LFSM_O"])
		self.s_LFSM_U = float(json_obj["s_LFSM_U"])
		self.slope_sp = float(json_obj["slope_sp"])
		self.V_deadband_sp = float(json_obj["V_deadband_sp"])
		# Gradient values (setpoint rate of change MW/sec or p.u/sample)
		self.P_grad = float(json_obj["P_grad"])/self.S_nom # p.u/sample
		self.MPPT_grad = float(json_obj["F_grad"])/self.S_nom # p.u/sample
		self.F_grad = float(json_obj["MPPT_grad"])/self.S_nom # p.u/sample
		# P control PID parameters
		self.p_kp = float(json_obj["p_kp"])  # Proportional gain
		self.p_ki = float(json_obj["p_ki"])  # Integral gain
		self.p_kd = float(json_obj["p_kd"])  # Derivative gain
		self.p_dt = float(json_obj["p_dt"])  # Integration/Derivation time constant
		# P control PID parameters
		self.q_kp = float(json_obj["q_kp"])  # Proportional gain
		self.q_ki = float(json_obj["q_ki"])  # Integral gain
		self.q_kd = float(json_obj["q_kd"])  # Derivative gain
		self.q_dt = float(json_obj["q_dt"])  # Integration/Derivation time constant
		# Simulation variables
		self.f_disturbance = 50.0 # Nominal Frequency = 50 Hz
		self.v_disturbance = 1.0 # Nominal Voltage = 1 p.u
		self.simulation_mode = 0 # 0 = voltage / 1 = frequency
		self.simulation_run_stop = 0 # 0 = stop / 1 = run
		self.simulation_duration = 0 # seconds
		self.simulation_start_stop = False # True = simulation ongoing / False = real measurments
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
		# Meteo
		self.gamma = 0.3
		self.temp = 30
		self.irradiance = 900
		self.sunrise = 600
		self.sunset = 2052
		# Q(P)
		self.PQ_curve = self.configdata["device"]["PQ_points"]
		self.numOfPoints = len(list(self.PQ_curve.values()))
		self.P_points = list(self.PQ_curve.values())
		self.Q_points = list(self.PQ_curve.keys())
		self.m = []
		# Q(U) with V Limit variables
		self.UQ_curve = self.configdata["device"]["UQ_points"]
		self.numOfPoints2 = 4 # by default
		self.U_points = list(self.UQ_curve.keys())
		self.Q_points2 = list(self.UQ_curve.values())
		self.P1 = [float(self.U_points[0]), float(self.Q_points2[0])]
		self.P2 = [float(self.U_points[1]), float(self.Q_points2[1])]
		self.P3 = [float(self.U_points[2]), float(self.Q_points2[2])]
		self.P4 = [float(self.U_points[3]), float(self.Q_points2[3])]
		self.ma = 0
		self.mb = 0
		self.dba = 0
		self.dbb = 0
		# Q(U) parameters
		self.QU_params = self.configdata["device"]["curve_params"]
		self.QU_db = float(self.QU_params["deadband"])
		self.QU_s = float(self.QU_params["slope"])
		self.QU_v = float(self.QU_params["v_ref"])
		self.QU_q = float(self.QU_params["q_ref"])
		self.PF_p = float(self.QU_params["p_ref"])
    
	def connect_to_slaves(self):
		checksum = 0
		index = 0
		for i in self.slaves_data:
			# print(i)
			self.slave_id.append(int(self.slaves_data[i]["ID"]))
			self.slaves_Pinst.append(int(self.slaves_data[i]["nominal_power"]))
			self.pi_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
			self.qi_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
			self.qa_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
			checksum += (int(self.slaves_data[i]["nominal_power"]))
			index += 1
        
		print(self.slave_id)
		print(self.slaves_Pinst)
		print(self.pi_per)

		if checksum != self.S_nom:
			print("Error! Sum of inverter's nominal power ratings does not match Slave's nominal power")
		else:
			print("Checksum ok")

	def simulation_countdown(self):
		for i in range(self.simulation_duration):
			if not (self.simulation_start_stop): break
			time.sleep(1)
		self.simulation_run_stop = 0
		self.simulation_start_stop = False
    
	def run_simulation(self, value):
		self.simulation_run_stop = value
		if self.simulation_run_stop == 1:
			self.simulation_start_stop = True
			clock = threading.Thread(target=self.simulation_countdown)
			clock.start()
		elif self.simulation_run_stop == 0:
			self.simulation_start_stop = False
    
	def V_Limit_VDE_init(self, q_ref):
		# Hard-coded points
		# P1 = [0.94, 0.2]
		# P2 = [0.96, 0.0]
		# P3 = [1.08, 0.0]
		# P4 = [1.10, -0.35]
		# Hard-coded points
		# P1 = [float(self.U_points[0]), float(self.Q_points2[0])]
		# P2 = [float(self.U_points[1]), float(self.Q_points2[1])]
		# P3 = [float(self.U_points[2]), float(self.Q_points2[2])]
		# P4 = [float(self.U_points[3]), float(self.Q_points2[3])]

		# Slopes are not affected by voltage setpoint
		self.ma = (self.P2[1] - self.P1[1]) / (self.P2[0] - self.P1[0])
		self.mb = (self.P4[1] - self.P3[1]) / (self.P4[0] - self.P3[0])

		# Deadband limits are affected by voltage setpoint
		self.dba = self.P2[0] + q_ref / self.ma
		self.dbb = self.P3[0] + q_ref / self.mb

		# print(f'ma = {round(self.ma, 2)}')
		# print(f'mb = {round(self.mb, 2)}')
		# print(f'dba = {round(self.dba, 2)}')
		# print(f'dbb = {round(self.dbb, 2)}')
		# print(f'qmax = {round(self.qmax, 2)}')
		# print(f'qmax = {round(self.qmin, 2)}')
    
	def QP_init(self):
		# P = [0, 0.1, 0.15, 0.2, 0.25, 0.5, 0.66, 0.75, 0.75, 0.9, 0.95, 1.0]
		# Q = [0, 0, 0.025, 0.025, 0.08, 0.1, 0.1, 0.12, 0.15, 0.16, 0.2, 0.2]
		# Calculate slopes
		for i in range(self.numOfPoints-1):
			num = float(self.Q_points[i+1]) - float(self.Q_points[i])
			den = float(self.P_points[i+1]) - float(self.P_points[i])
			if den == 0: slope = 0
			else: slope = num/den
			self.m.append(slope)
    
	def set_sp(self):
		# Local setpoints
		if self.local_remote == 0:
			if self.p_mode == 3: self.p_ex_sp = self.max_P_cap
			else: self.p_ex_sp = self.local_P_sp
			self.q_ex_sp = self.local_Q_sp
			self.pf_ex_sp = self.local_PF_sp
		# Remote setpoints
		elif self.local_remote == 1:
			if self.p_mode == 3:
				self.p_ex_sp = self.max_P_cap
			else:
				if self.tso_P_sp <= self.fose_P_sp: self.remote_P_sp = self.tso_P_sp
				else: self.remote_P_sp = self.fose_P_sp
			if self.tso_Q_sp <= self.fose_Q_sp: self.remote_Q_sp = self.tso_Q_sp
			else: self.remote_Q_sp = self.fose_Q_sp
			self.p_ex_sp = self.remote_P_sp
			self.q_ex_sp = self.remote_Q_sp
			self.pf_ex_sp = self.remote_PF_sp
        
		# Check operational state
		if self.operational_state == 1:
			self.p_ex_sp = 0
			self.q_ex_sp = 0
			self.p_mode = 0
			self.q_mode = 0
		
