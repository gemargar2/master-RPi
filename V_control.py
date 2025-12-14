
printMessages = False

v_ref = 1.0 # Voltage setpoint is always 1.0 p.u

# Q mode = 2
def V_control(ppc_master_obj):
	q_ref = 0 # ppc_master_obj.q_ex_sp
	v_actual = ppc_master_obj.v_actual
	
	if ppc_master_obj.local_remote == 0: v_sp = ppc_master_obj.local_V_sp # setpoint voltage
	else: v_sp = ppc_master_obj.remote_V_sp # setpoint voltage
	
	slope = ppc_master_obj.slope_sp # Droop adjustable between 2-12%, default value 5%
	db = ppc_master_obj.V_deadband_sp # voltage deadband
	m = 1/slope # gradient 7<m<24
	
	if (v_actual < v_sp - db):
		if printMessages:
			print(f'{v_actual} < {v_sp - db}')
			print("Under voltage")
		delta_V = (v_sp - db) - v_actual
		delta_Q = delta_V * m
		q_in_sp = q_ref + delta_Q
	elif (v_actual > v_sp + db):
		if printMessages:
			print(f'{v_actual} > {v_sp + db}')
			print("Over voltage")
		delta_V = v_actual - (v_sp + db)
		delta_Q = delta_V * m
		q_in_sp = q_ref - delta_Q
	else:
		q_in_sp = q_ref
	
	if q_in_sp >= 0.33: q_in_sp = 0.33
	elif q_in_sp <= -0.33: q_in_sp = -0.33
	return q_in_sp

# Q mode = 3 (PF Control)
# Q mode = 4 (Q Open Loop)

# Q mode = 5
def QU_VDE(ppc_master_obj):
	q_ref = 0 # ppc_master_obj.q_ex_sp
	v_actual = ppc_master_obj.v_actual
	slope = ppc_master_obj.QU_s # Droop adjustable between 2-12%, default value 5%
	v_sp = ppc_master_obj.QU_v # setpoint voltage
	db = ppc_master_obj.QU_db # voltage deadband
	m = 1/slope # gradient 7<m<24
	#print(f'slope = {slope}, v_sp = {v_sp}, db = {db}, m = {m}')

	if (v_actual < v_sp - db):
		if printMessages:
			print(f'{v_actual} < {v_sp - db}')
			print("Under voltage")
		delta_V = (v_sp - db) - v_actual
		delta_Q = delta_V * m
		q_in_sp = q_ref + delta_Q
	elif (v_actual > v_sp + db):
		if printMessages:
			print(f'{v_actual} > {v_sp + db}')
			print("Over voltage")
		delta_V = v_actual - (v_sp + db)
		delta_Q = delta_V * m
		q_in_sp = q_ref - delta_Q
	else:
		q_in_sp = q_ref

	if q_in_sp >= 0.33: q_in_sp = 0.33
	elif q_in_sp <= -0.33: q_in_sp = -0.33
	#print(f'Q({v_actual}) = {q_in_sp}')	
	
	return q_in_sp

# Q mode = 6
def V_Limit_VDE(ppc_master_obj):
	q_ref = ppc_master_obj.QU_q
	v_actual = ppc_master_obj.v_actual
	if (v_actual < ppc_master_obj.dba):
		if printMessages:
			print(f'{v_actual} < {ppc_master_obj.dba}')
			print("Under voltage")
		delta_V = ppc_master_obj.dba - v_actual
		delta_Q = delta_V * abs(ppc_master_obj.ma)
		q_in_sp = q_ref + delta_Q
	elif (v_actual > ppc_master_obj.dbb):
		if printMessages:
			print(f'{v_actual} > {ppc_master_obj.dbb}')
			print("Over voltage")
		delta_V = v_actual - ppc_master_obj.dbb
		delta_Q = delta_V * abs(ppc_master_obj.mb)
		q_in_sp = q_ref - delta_Q
	else:
		q_in_sp = q_ref
	
	if q_in_sp >= 0.33: q_in_sp = 0.33
	elif q_in_sp <= -0.33: q_in_sp = -0.33
	#print(f'Q({v_actual}) = {q_in_sp}')
	return q_in_sp

# V limit VDE init
def V_Limit_VDE_init(self, q_ref):
	#print(f'P1=({self.P1[0]}, {self.P1[1]}), P2=({self.P2[0]}, {self.P2[1]}), P3=({self.P3[0]}, {self.P3[1]}), P4=({self.P4[0]}, {self.P4[1]})')
	# Slopes are not affected by voltage setpoint
	self.ma = (self.P2[1] - self.P1[1]) / (self.P2[0] - self.P1[0])
	self.mb = (self.P4[1] - self.P3[1]) / (self.P4[0] - self.P3[0])
	# Deadband limits are affected by voltage setpoint
	self.dba = self.P2[0] + q_ref / self.ma
	self.dbb = self.P3[0] + q_ref / self.mb
	#print(f'ma = {round(self.ma, 2)}')
	#print(f'mb = {round(self.mb, 2)}')
	#print(f'dba = {round(self.dba, 2)}')
	#print(f'dbb = {round(self.dbb, 2)}')
	#print(f'qmax = {round(self.max_Q_cap, 2)}')
	#print(f'qmax = {round(self.min_Q_cap, 2)}')

# Q(P) init
def QP_init(self):
	# Calculate slopes
	for i in range(self.numOfPoints-1):
		num = float(self.Q_points[i+1]) - float(self.Q_points[i])
		den = float(self.P_points[i+1]) - float(self.P_points[i])
		if den == 0: slope = 0
		else: slope = num/den
		self.m.append(slope)
