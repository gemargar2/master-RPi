import zmq
import time
import threading
from numpy import zeros
from V_control import *

class PPC_master_class:
	def __init__(self, json_obj, json_mem):
		# --- Configuration ----------------------------
		self.configdata = json_obj
		self.memory = json_mem
		self.boot_flag = self.memory["boot_flag"]
		# General description
		self.name = self.configdata["master"]["name"]
		self.desc = self.configdata["master"]["description"]
		self.type = self.configdata["master"]["plant_type"]
		self.surface_type = self.configdata["master"]["surface_type"]
		self.surface_tilt = self.configdata["master"]["surface_tilt"]
		self.surface_azimuth = self.configdata["master"]["surface_azimuth"]
		self.solar_zenith = self.configdata["master"]["solar_zenith"]
		self.solar_azimuth = self.configdata["master"]["solar_azimuth"]
		self.temp_coef = self.configdata["master"]["temp_coefficient_of_power"]
		# Nominal ratings
		self.S_nom = float(self.configdata["master"]["nominal_power"]) # Nominal apparent power in MVA
		self.P_nom = float(self.configdata["master"]["nominal_power"]) # Nominal active power in MW
		self.V_nom = float(self.configdata["master"]["nominal_voltage"]) # Nominal voltage in kV
		self.sampling_rate = 20 # Hz = 20 samples/second
		# Slave PPCs management
		self.slaves_data = self.configdata["slave_tree"]
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
		self.connection = 0 # connection status
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
		# Limits
		self.start_stop = 0 # 0 = start / 1 = stop
		self.operational_state = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.release = True # False = PPC has turned off due to grid imbalance / True = PPC is ready to reconnect
		self.f_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.v_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.v2_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.v3_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.auto_start_state = 0 # 0 = OFF / 1 = ON
		# Main switch
		self.main_switch_pos = 1 # 0 = Open / 1 = Closed
		# Timers / coutners
		self.f_counter = 0
		self.v_counter = 0
		self.v2_counter = 0
		self.v3_counter = 0
		self.release_counter = 0
		# Local setpoints (SCADA)
		self.local_P_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_P_sp"]/self.S_nom
		self.local_Q_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_Q_sp"]/self.S_nom
		self.local_PF_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_PF_sp"]
		self.local_V_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_V_sp"]/self.V_nom
		# Remote setpoints (TSO)
		self.remote_P_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_P_sp"]/self.S_nom
		self.remote_Q_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_Q_sp"]/self.S_nom
		self.remote_PF_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_PF_sp"]
		self.remote_V_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_V_sp"]/self.V_nom
		# Network Operator setpoints (TSO)
		self.tso_P_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_P_sp"]/self.S_nom # Minimum p.u
		self.tso_Q_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_Q_sp"]/self.S_nom # Minimum p.u
		self.tso_V_sp = 0 # Maximum p.u
		self.tso_PF_sp = 0 # Maximum p.u
		# 3rd party setpoints (FOSE)
		self.fose_P_sp = -0.1 # Maximum p.u
		self.fose_Q_sp = 0.05 # Maximum p.u
		self.fose_V_sp = 0 # Maximum p.u
		self.fose_PF_sp = 0 # Maximum p.u
		# Universal setpoints (configured by SCADA)
		# Gradient values (setpoint rate of change MW/sec or p.u/sample)
		self.P_grad = self.configdata["PPC_parameters"]["power_gradients"]["P_grad"]/self.S_nom # p.u/sample
		self.F_grad = self.configdata["PPC_parameters"]["power_gradients"]["F_grad"]/self.S_nom # p.u/sample
		self.MPPT_grad = self.configdata["PPC_parameters"]["power_gradients"]["MPPT_grad"]/self.S_nom # p.u/sample
		self.Q_grad = 1 # 1 p.u/sample => reactive power can change immediately
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
		# Simulation variables
		self.f_disturbance = 50.0 # Nominal Frequency = 50 Hz
		self.v_disturbance = 1.0 # Nominal Voltage = 1 p.u
		self.simulation_mode = 0 # 0 = voltage / 1 = frequency
		self.simulation_run_stop = 0 # 0 = stop / 1 = run
		self.simulation_duration = 0 # seconds
		self.simulation_start_stop = False # True = simulation ongoing / False = real measurments
		# ----------------------- Setpoints -------------------------------------
		# External setpoints (init with local values)
		self.p_ex_sp = self.local_P_sp
		self.q_ex_sp = self.local_Q_sp
		self.pf_ex_sp = self.local_PF_sp
		# Internal setpoints
		self.p_in_sp = 0
		self.q_in_sp = 0
		# Setpoints with gradient
		self.p_grad_sp = 0
		self.q_grad_sp = 0
		# Setpoints with PID
		self.p_pid_sp = 0
		self.q_pid_sp = 0
		# ----------------------- Measurements -------------------------------------
		# HV meter
		self.p_actual_hv = 0
		self.q_actual_hv = 0
		self.f_actual = 50
		self.v_actual = 1
		self.v2_actual = 1
		self.v3_actual = 1
		self.pf_actual = 1
		# MV meter main
		self.p_actual_mv = 0
		self.q_actual_mv = 0
		# Global Meteo
		self.temp = 30
		self.irradiance = 900
		# Settling time
		self.start = 0
		# ----------------------- Control curves ----------------------------------
		# P(f)
		self.s_FSM = self.configdata["PPC_parameters"]["P(f)_curve"]["s_FSM"]
		self.s_LFSM_O = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_O"]
		self.s_LFSM_U = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_U"]
		self.PF_p = self.configdata["PPC_parameters"]["P(f)_curve"]["p_ref"]
		# Q(P)
		self.numOfPoints = len(self.configdata["PPC_parameters"]["Q(P)_curve"]["P_values"])
		self.P_points = self.configdata["PPC_parameters"]["Q(P)_curve"]["P_values"]
		self.Q_points = self.configdata["PPC_parameters"]["Q(P)_curve"]["Q_values"]
		self.m = []
		self.QP_init()
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
		self.initialize_setpoints()
	
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
		start = time.time()
		while self.simulation_start_stop:
			time.sleep(0.1)
			end = time.time()
			# print(f'{end-start} > {self.simulation_duration}')
			if end-start >= self.simulation_duration:
				# print("Hello")
				self.simulation_start_stop = False
				break
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
	
	# Control curves
	
	V_Limit_VDE_init = V_Limit_VDE_init
	QP_init = QP_init
    
	def setpoint_priority(self):
		printMessages = False
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
				# Both negative
				if self.tso_P_sp < 0 and self.fose_P_sp < 0:
					if printMessages: print("Both negative")
					self.remote_P_sp = 0
				# One positive one negative
				elif self.tso_P_sp < 0 and self.fose_P_sp > 0:
					if printMessages: print(f"tso={self.tso_P_sp}<0 / fose={self.fose_P_sp}>0")
					self.remote_P_sp = self.fose_P_sp #/self.S_nom
				elif self.tso_P_sp > 0 and self.fose_P_sp < 0:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}<0")
					self.remote_P_sp = self.tso_P_sp #/self.S_nom
				# Both setpoints are positive
				elif self.tso_P_sp <= self.fose_P_sp:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}>0")
					if printMessages: print("0<tso<fose")
					self.remote_P_sp = self.tso_P_sp #/self.S_nom
				else:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}>0")
					if printMessages: print("0<fose<tso")
					self.remote_P_sp = self.fose_P_sp #/self.S_nom
			# Q setpoint
			if self.tso_Q_sp <= self.fose_Q_sp: self.remote_Q_sp = self.tso_Q_sp #/self.S_nom
			else: self.remote_Q_sp = self.fose_Q_sp #/self.S_nom
			self.p_ex_sp = self.remote_P_sp
			self.q_ex_sp = self.remote_Q_sp
			self.pf_ex_sp = self.remote_PF_sp
        
		# Check operational state
		if self.operational_state == 1:
			self.p_ex_sp = 0
			self.q_ex_sp = 0
			self.p_mode = 0
			self.q_mode = 0

	def set_start_zero(self):
		message1 = { "destination": "localPlatform", "value": "0", "value_name": "Start" }
		message2 = { "destination": "localPlatform", "value": "1", "value_name": "Stop" }
		try:
			self.socket_tx.send_json(message1, zmq.NOBLOCK)
			self.socket_tx.send_json(message2, zmq.NOBLOCK)
		except Exception as e:
			print("Send failed:", e)
			traceback.print_exc()
	
	def initialize_setpoints(self):
		if self.boot_flag == 1:
			# Local setpoints (SCADA)
			self.local_P_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_P_sp"]/self.S_nom
			self.local_Q_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_Q_sp"]/self.S_nom
			self.local_PF_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_PF_sp"]
			self.local_V_sp = self.configdata["PPC_parameters"]["local_setpoints"]["local_V_sp"]/self.V_nom
			# Remote setpoints (TSO)
			self.remote_P_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_P_sp"]/self.S_nom
			self.remote_Q_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_Q_sp"]/self.S_nom
			self.remote_PF_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_PF_sp"]
			self.remote_V_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_V_sp"]/self.V_nom
			# Network Operator setpoints (TSO)
			self.tso_P_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_P_sp"]/self.S_nom # Minimum p.u
			self.tso_Q_sp = self.configdata["PPC_parameters"]["remote_setpoints"]["remote_Q_sp"]/self.S_nom # Minimum p.u
		else:
			# Local setpoints (SCADA)
			self.local_P_sp = self.memory["local_setpoints"]["local_P_sp"]/self.S_nom
			self.local_Q_sp = self.memory["local_setpoints"]["local_Q_sp"]/self.S_nom
			self.local_PF_sp = self.memory["local_setpoints"]["local_PF_sp"]
			self.local_V_sp = self.memory["local_setpoints"]["local_V_sp"]/self.V_nom
			# Remote setpoints (TSO)
			self.remote_P_sp = self.memory["remote_setpoints"]["remote_P_sp"]/self.S_nom
			self.remote_Q_sp = self.memory["remote_setpoints"]["remote_Q_sp"]/self.S_nom
			self.remote_PF_sp = self.memory["remote_setpoints"]["remote_PF_sp"]
			self.remote_V_sp = self.memory["remote_setpoints"]["remote_V_sp"]/self.V_nom
			# Network Operator setpoints (TSO)
			self.tso_P_sp = self.memory["remote_setpoints"]["remote_P_sp"]/self.S_nom # Minimum p.u
			self.tso_Q_sp = self.memory["remote_setpoints"]["remote_Q_sp"]/self.S_nom # Minimum p.u
					
					
					