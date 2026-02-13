import zmq
import time
import threading
from aux_classes import *
from numpy import zeros
from V_control import *
from class_methods import *
from collections import deque

sampling_rate = 10 # 20Hz
time_window = 30 # 30 seconds
smax = time_window*sampling_rate # samples

class PPC_master_class:
	def __init__(self, json_obj, json_mem):
		# --- Configuration ----------------------------
		self.configdata = json_obj
		self.memory = json_mem
		self.boot_flag = 0 # 0 = Init setpoints from memory / 1 = Init setpoints from config
		# General description
		self.name = self.configdata["master"]["name"]
		# Nominal ratings
		self.S_nom = float(self.configdata["master"]["nominal_power"]) # Nominal apparent power in MVA
		self.V_nom = float(self.configdata["master"]["nominal_voltage"]) # Nominal voltage in kV
		self.sampling_rate = 10 # Hz = 20 samples/second => period = 1/20 = 0.05s (50ms)
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
		self.slave_p_sp = zeros(self.numberOfSlaves) # P setpoint distributionl
		self.slave_q_sp = zeros(self.numberOfSlaves) # Q setpoint distribution
		# Summary
		self.total_pmax = 0 # MW
		self.total_qmax = 0 # MVAR
		self.total_qmin = 0 # MVAR
		self.connection = 0 # connection status
		# ---------------------------------------------------------------
		# ----------------------- ZMQ -----------------------------------
		# ---------------------------------------------------------------
		# --- Establish connection for signal transmission --------------
		self.context_tx = zmq.Context()
		self.socket_tx = self.context_tx.socket(zmq.PUSH)
		self.socket_tx.bind("ipc:///tmp/zmqsub")
		# --- Establish connection for signal reception --------------
		self.context_rx = zmq.Context()
		self.socket_rx = self.context_rx.socket(zmq.PULL)
		self.socket_rx.connect("ipc:///tmp/zmqpub")
		time.sleep(5)
		# --- Signals ----------------------------
		# Local = SCADA / Remote = TSO/FOSE
		self.local_remote = 0 # 0 = Local / 1 = Remote
		# Mode of operation for active and reactive control
		self.p_mode = 0 # 0 = P control (PID) / 1 = F control (FSM) / 2 = P Open Loop / 3 = MPPT control
		self.q_mode = 5 # 0 = Q control (PID) / 1 = Q(P) control / 2 = V control / 3 = PF control / 4 = Q Open Loop / 5 = Q(U) / 6 = Q(U) with limit	
		# Per unit values
		self.max_P_cap = 1 # Max active power capability (meteo are ignored)
		self.max_Q_cap = 0.33 # Max reactive power capability
		self.min_Q_cap = -0.33 # Max reactive power capability
		# -----------------------------------------------------------------------
		# ----------------------- Setpoints -------------------------------------
		# -----------------------------------------------------------------------
		# Local setpoints (SCADA)
		self.local_sp = setpoints()
		# Remote setpoints (TSO vs FOSE)
		self.remote_sp = setpoints()
		# Network Operator setpoints (TSO)
		self.tso_sp = setpoints()
		# 3rd party setpoints (FOSE)
		self.fose_sp = setpoints()
		# External setpoints (init with local values)
		self.ex_sp = setpoints()
		# Gradient values (setpoint rate of change MW/sec or p.u/sample)
		# 0.66%*Pbinst/sec = 0.0066/(20*0.05) = 0.000330 p.u/sample
		# 0.33%*Pbinst/sec = 0.0033/(20*0.05) = 0.000165 p.u/sample
		# 4%*Pbinst/min = 0.04/(60*20*0.05) = 0.0000333 p.u/sample
		# 10%*Pbinst/min = 0.10/(60*20*0.05) = 0.0000833 p.u/sample
		self.P_grad = 0
		self.F_grad = 0
		self.MPPT_grad = 0
		# P control PID parameters
		self.p_pid = pid_params()
		# Q control PID parameters
		self.q_pid = pid_params()
		# Simulation variables
		self.f_disturbance = 50 # Nominal Frequency = 50 Hz
		self.v_disturbance = 1 # Nominal Voltage = 1 p.u
		self.simulation_mode = 0 # 0 = voltage / 1 = frequency
		self.simulation_run_stop = 0 # 0 = stop / 1 = run
		self.simulation_duration = 0 # seconds
		self.simulation_start_stop = False # True = simulation ongoing / False = real measurments
		self.watchdog = True
		# -----------------------------------------------------------------------
		# ----------------------- Submodules ------------------------------------
		# -----------------------------------------------------------------------
		# Internal setpoints
		self.p_in_sp = 0
		self.q_in_sp = 0
		self.prev_p_in_sp = 0
		self.prev_q_in_sp = 0
		# Gradient submodule
		self.grad_submod = basic_submod()
		# PID submodule
		self.pid_submod = basic_submod()
		# Reactive power step change
		self.delta_q = 0
		# -----------------------------------------------------------------------
		# ----------------------- Measurements ----------------------------------
		# -----------------------------------------------------------------------
		# HV meter
		self.hv_meter = HV_meter_class()
		# self.p_actual_hv = 0
		# self.q_actual_hv = 0
		# self.s_actual_hv = 0
		# self.f_actual = 50
		# self.vab_actual = 1
		# self.vbc_actual = 1
		# self.vca_actual = 1
		# self.v_actual = 1
		# self.pf_actual = 1
		# MV meter main
		self.p_actual_mv = 0
		self.q_actual_mv = 0
		# Global Meteo
		self.temp = 30
		self.irradiance = 900
		# Limits
		self.start_stop = 0 # 0 = start / 1 = stop
		self.operational_state = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.release = True # False = PPC has turned off due to grid imbalance / True = PPC is ready to reconnect
		self.f_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.vab_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.vbc_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.vca_shutdown = 0 # 0 = Running / 1 = Not Running / 2 = Stopping / 3 = Error
		self.auto_start_state = 0 # 0 = OFF / 1 = ON
		# Timers / counters
		self.f_counter = 0
		self.vab_counter = 0
		self.vbc_counter = 0
		self.vca_counter = 0
		self.release_counter = 0
		# ------- Characteristics curves ----------------------------------
		# ------- Signal driven -------------------------------------------
		# P(f)
		self.s_FSM = self.configdata["PPC_parameters"]["P(f)_curve"]["s_FSM"]
		self.s_LFSM_O = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_O"]
		self.s_LFSM_U = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_U"]
		self.fsm_pref_flag = True
		self.lfsm_pref_flag = True
		self.vde4130_flag = False # Test 12: True = Priority of LFSM over TSO / False = Priority of TSO over LFSM
		self.tso_none_flag = True # Test 12: True = TSO is not / False = Priority of TSO over LFSM
		self.lfsm_flag = False
		self.fsm_pref = 0.5
		self.lfsm_pref = 0.5
		# V control
		self.slope_sp = self.configdata["PPC_parameters"]["V_control_curve"]["slope_sp"]
		self.V_deadband_sp = self.configdata["PPC_parameters"]["V_control_curve"]["V_deadband_sp"]
		# ------- Config tool driven -------------------------------------------
		# Q(P)
		self.numOfPoints = len(self.configdata["PPC_parameters"]["Q(P)_curve"]["P_values"])
		self.P_points = self.configdata["PPC_parameters"]["Q(P)_curve"]["P_values"]
		self.Q_points = self.configdata["PPC_parameters"]["Q(P)_curve"]["Q_values"]
		self.m = []
		# Q(U)
		self.QU_db = self.configdata["PPC_parameters"]["Q(U)_curve"]["deadband"]
		self.QU_s = self.configdata["PPC_parameters"]["Q(U)_curve"]["slope"]
		# Q(U) w/Limit
		self.numOfPoints2 = 4 # by default
		self.U_points = self.configdata["PPC_parameters"]["Q(U)_Limit_curve"]["U_values"]
		self.Q_points2 = self.configdata["PPC_parameters"]["Q(U)_Limit_curve"]["Q_values"]
		self.P1 = [float(self.U_points[0]), float(self.Q_points2[0])]
		self.P2 = [float(self.U_points[1]), float(self.Q_points2[1])]
		self.P3 = [float(self.U_points[2]), float(self.Q_points2[2])]
		self.P4 = [float(self.U_points[3]), float(self.Q_points2[3])]
		self.ma = 0
		self.mb = 0
		self.dba = 0
		self.dbb = 0
		# ------- Plot vectors -------------------------------------------------
		self.sample = 0 # samples
		self.x = 0 # samples
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
		# ---- Run init functions --------------------------------
		self.QP_init()
		self.V_Limit_VDE_init()
		self.connect_to_slaves()
		self.initialize_setpoints()
		self.setpoint_priority()
	
	connect_to_slaves = connect_to_slaves
	V_Limit_VDE_init = V_Limit_VDE_init
	QP_init = QP_init
	setpoint_priority = setpoint_priority
	initialize_setpoints = initialize_setpoints
	set_start_zero = set_start_zero
	
					