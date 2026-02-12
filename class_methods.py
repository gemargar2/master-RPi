# Connect to slaves
import zmq
import traceback

def set_start_zero(self):
	message1 = { "destination": "localPlatform", "value": "0", "value_name": "Start" }
	message2 = { "destination": "localPlatform", "value": "1", "value_name": "Stop" }
	try:
		self.socket_tx.send_json(message1, zmq.NOBLOCK)
		self.socket_tx.send_json(message2, zmq.NOBLOCK)
	except Exception as e:
		print("Send failed:", e)
		traceback.print_exc()

def connect_to_slaves(self):
	checksum = 0
	index = 0
	for i in self.slaves_data:
		# print(i)
		self.slave_id.append(int(self.slaves_data[i]["ID"]))
		self.slaves_Pinst.append(float(self.slaves_data[i]["nominal_power"]))
		self.pi_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
		self.qi_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
		self.qa_per[index] = float(self.slaves_data[i]["nominal_power"])/self.S_nom
		checksum += (float(self.slaves_data[i]["nominal_power"]))
		index += 1
	
	#print(self.slave_id)
	#print(self.slaves_Pinst)
	#print(self.pi_per)
	
	if checksum != self.S_nom:
		print("Error! Sum of inverter's nominal power ratings does not match Slave's nominal power")
	else:
		print("Slave PPC connected successfully")

def initialize_setpoints(self):
	# ------ Signal based parameters ---------------------------
	self.local_remote = self.memory["local_remote"]
	# Local setpoints (SCADA)
	self.local_setpoints.P_sp = self.memory["local_setpoints"]["local_P_sp"]
	self.local_setpoints.Q_sp = self.memory["local_setpoints"]["local_Q_sp"]
	self.local_setpoints.PF_sp = self.memory["local_setpoints"]["local_PF_sp"]
	self.local_setpoints.V_sp = self.memory["local_setpoints"]["local_V_sp"]
	# Network operator setpoints (TSO)
	self.tso_P_sp = self.memory["tso_setpoints"]["tso_P_sp"]
	self.tso_Q_sp = self.memory["tso_setpoints"]["tso_Q_sp"]
	self.tso_PF_sp = self.memory["tso_setpoints"]["tso_PF_sp"]
	self.tso_V_sp = self.memory["tso_setpoints"]["tso_V_sp"]
	# Third Party setpoints (FOSE)
	self.fose_P_sp = self.memory["fose_setpoints"]["fose_P_sp"]
	self.fose_Q_sp = self.memory["fose_setpoints"]["fose_Q_sp"]
	self.fose_PF_sp = self.memory["fose_setpoints"]["fose_PF_sp"]
	self.fose_V_sp = self.memory["fose_setpoints"]["fose_V_sp"]
	# Memory of the internal setpoints in case of power supply fault
	self.p_in_sp = self.memory["internal_setpoints"]["p_in_sp"]
	self.q_in_sp = self.memory["internal_setpoints"]["q_in_sp"]
	self.p_grad_sp = self.memory["internal_setpoints"]["p_grad_sp"]
	self.q_grad_sp = self.memory["internal_setpoints"]["q_grad_sp"]
	self.p_pid_sp = self.memory["internal_setpoints"]["p_pid_sp"]
	self.q_pid_sp = self.memory["internal_setpoints"]["q_pid_sp"]
	self.prev_p_grad_sp = self.memory["internal_setpoints"]["prev_p_grad_sp"]
	self.prev_q_grad_sp = self.memory["internal_setpoints"]["prev_q_grad_sp"]
	self.prev_p_pid_sp = self.memory["internal_setpoints"]["prev_p_pid_sp"]
	self.prev_q_pid_sp = self.memory["internal_setpoints"]["prev_q_pid_sp"]
	self.p_mode = self.memory["control_mode"]["active_control_mode"]
	self.q_mode = self.memory["control_mode"]["reactive_control_mode"]
	# Config file vs Memory
	# PPC Parameters (PID weights, Gradient and Characteristics)
	if self.boot_flag == 1:
		# Gradients
		self.P_grad = self.configdata["PPC_parameters"]["power_gradients"]["P_grad"]# p.u/sample
		self.F_grad = self.configdata["PPC_parameters"]["power_gradients"]["F_grad"] # p.u/sample
		self.MPPT_grad = self.configdata["PPC_parameters"]["power_gradients"]["MPPT_grad"] # p.u/sample
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
		# P(f)
		self.s_FSM = self.configdata["PPC_parameters"]["P(f)_curve"]["s_FSM"]
		self.s_LFSM_O = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_O"]
		self.s_LFSM_U = self.configdata["PPC_parameters"]["P(f)_curve"]["s_LFSM_U"]
		# V control
		self.slope_sp = self.configdata["PPC_parameters"]["V_control_curve"]["slope_sp"]
		self.V_deadband_sp = self.configdata["PPC_parameters"]["V_control_curve"]["V_deadband_sp"]
	else:
		# Gradients
		self.P_grad = self.memory["power_gradients"]["P_grad"] # p.u/sample
		self.F_grad = self.memory["power_gradients"]["F_grad"] # p.u/sample
		self.MPPT_grad = self.memory["power_gradients"]["MPPT_grad"] # p.u/sample
		# P control PID parameters
		self.p_kp = self.memory["P_PID_parameters"]["p_kp"] # Proportional gain
		self.p_ki = self.memory["P_PID_parameters"]["p_ki"] # Integral gain
		self.p_kd = self.memory["P_PID_parameters"]["p_kd"] # Derivative gain
		self.p_dt = self.memory["P_PID_parameters"]["p_dt"] # Integration/Derivation time constant
		# P control PID parameters
		self.q_kp = self.memory["Q_PID_parameters"]["q_kp"] # Proportional gain
		self.q_ki = self.memory["Q_PID_parameters"]["q_ki"] # Integral gain
		self.q_kd = self.memory["Q_PID_parameters"]["q_kd"] # Derivative gain
		self.q_dt = self.memory["Q_PID_parameters"]["q_dt"] # Integration/Derivation time constant
		# P(f)
		self.s_FSM = self.memory["P(f)_curve"]["s_FSM"]
		self.s_LFSM_O = self.memory["P(f)_curve"]["s_LFSM_O"]
		self.s_LFSM_U = self.memory["P(f)_curve"]["s_LFSM_U"]
		# V control
		self.slope_sp = self.memory["V_control_curve"]["slope_sp"]
		self.V_deadband_sp = self.memory["V_control_curve"]["V_deadband_sp"]

def setpoint_priority(self):
		printMessages = False
		# Local setpoints
		if self.local_remote == 0:
			if self.p_mode == 3: value = self.max_P_cap
			else: value = self.local_setpoints.P_sp
			self.p_ex_sp = value
			self.q_ex_sp = self.local_setpoints.Q_sp
			self.v_ex_sp = self.local_setpoints.V_sp
			self.pf_ex_sp = self.local_setpoints.PF_sp
		
		# Remote setpoints
		elif self.local_remote == 1:
			if self.p_mode == 3:
				self.remote_P_sp = self.max_P_cap
			else:
				# Both negative
				if self.tso_P_sp < 0 and self.fose_P_sp < 0:
					if printMessages: print("Both negative")
					self.tso_none_flag = True
					self.remote_P_sp = self.local_P_sp
					self.remote_Q_sp = self.local_Q_sp
					self.remote_V_sp = self.local_V_sp
					self.remote_PF_sp = self.local_PF_sp
				# One positive one negative
				elif self.tso_P_sp < 0 and self.fose_P_sp > 0:
					if printMessages: print(f"tso={self.tso_P_sp}<0 / fose={self.fose_P_sp}>0")
					self.tso_none_flag = True
					self.remote_P_sp = self.fose_P_sp
					self.remote_Q_sp = self.fose_Q_sp
					self.remote_V_sp = self.fose_V_sp
					self.remote_PF_sp = self.fose_PF_sp
				elif self.tso_P_sp > 0 and self.fose_P_sp < 0:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}<0")
					self.tso_none_flag = False
					self.remote_P_sp = self.tso_P_sp
					self.remote_Q_sp = self.tso_Q_sp
					self.remote_V_sp = self.tso_V_sp
					self.remote_PF_sp = self.tso_PF_sp
				# Both setpoints are positive
				elif self.tso_P_sp <= self.fose_P_sp:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}>0")
					if printMessages: print("0<tso<fose")
					self.tso_none_flag = False
					self.remote_P_sp = self.tso_P_sp
					self.remote_Q_sp = self.tso_Q_sp
					self.remote_V_sp = self.tso_V_sp
					self.remote_PF_sp = self.tso_PF_sp
				elif self.fose_P_sp <= self.tso_P_sp:
					if printMessages: print(f"tso={self.tso_P_sp}>0 / fose={self.fose_P_sp}>0")
					self.tso_none_flag = False
					if self.lfsm_flag and not(self.vde4130_flag):
						if printMessages: print(f"Under LFSM mode TSO has the absolute priority")
						self.remote_P_sp = self.tso_P_sp
						self.remote_Q_sp = self.tso_Q_sp
						self.remote_V_sp = self.tso_V_sp
						self.remote_PF_sp = self.tso_PF_sp
					else:
						if printMessages: print("0<fose<tso")
						self.remote_P_sp = self.fose_P_sp
						self.remote_Q_sp = self.fose_Q_sp
						self.remote_V_sp = self.fose_V_sp
						self.remote_PF_sp = self.fose_PF_sp
				else:
					pass
			
			# Remote setpoint
			self.p_ex_sp = self.remote_P_sp
			self.q_ex_sp = self.remote_Q_sp
			self.v_ex_sp = self.remote_V_sp
			self.pf_ex_sp = self.remote_PF_sp
			