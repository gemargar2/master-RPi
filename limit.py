# Timeouts in seconds for testing
# For real-life multiply by 60 to get minutes
f_timer = 30
v_timer = 60
release_timer = 10

def normal_op_limits(ppc_master_obj, window_obj):
	# print(f'freq = {ppc_master_obj.f_actual}')
	# Frequency ranges
	if 49.0 <= ppc_master_obj.f_actual <= 51.0:
		window_obj.ax2.set_title("Frequency")
		ppc_master_obj.f_counter = 0
		ppc_master_obj.f_shutdown = 0 # Runninng
	elif 47.5 <= ppc_master_obj.f_actual < 49.0:
		window_obj.ax2.set_title(u"Underfrequency: shutdown in {}".format(f_timer-ppc_master_obj.f_counter))
		ppc_master_obj.f_counter += 1
		ppc_master_obj.f_shutdown = 2 # Stopping
	elif 51.0 < ppc_master_obj.f_actual <= 51.5:
		window_obj.ax2.set_title(u"Overfrequency: shutdown in {}".format(f_timer-ppc_master_obj.f_counter))
		ppc_master_obj.f_counter += 1
		ppc_master_obj.f_shutdown = 2 # Stopping
	elif ppc_master_obj.f_actual < 47.5 or ppc_master_obj.f_actual > 51.5:
		window_obj.ax2.set_title('Frequency out of range!')
		ppc_master_obj.f_shutdown = 1 # Not Running
	
	# if ppc_master_obj.f_actual < 49.8 or ppc_master_obj.f_actual > 50.2:
	if ppc_master_obj.f_actual > 50.2:
		ppc_master_obj.p_mode = 1

	# Voltage ranges phase 1
	if 0.90 <= ppc_master_obj.v_actual <= 1.118:
		window_obj.ax4.set_title('Voltage')
		ppc_master_obj.v_counter = 0
		ppc_master_obj.v_shutdown = 0 # Running
	elif 0.85 <= ppc_master_obj.v_actual < 0.90:
		window_obj.ax4.set_title(u"Undervoltage: shutdown in {}".format(v_timer-ppc_master_obj.v_counter))
		ppc_master_obj.v_counter += 1
		ppc_master_obj.v_shutdown = 2 # Stopping
	elif 1.118 < ppc_master_obj.v_actual <= 1.15:
		window_obj.ax4.set_title(u"Overvoltage: shutdown in {}".format(v_timer-ppc_master_obj.v_counter))
		ppc_master_obj.v_counter += 1
		ppc_master_obj.v_shutdown = 2 # Stopping
	elif ppc_master_obj.v_actual < 0.85 or ppc_master_obj.v_actual > 1.15:
		window_obj.ax4.set_title('Voltage out of range!')
		ppc_master_obj.v_shutdown = 1 # Not Running

	# Voltage ranges phase 2
	if 0.90 <= ppc_master_obj.v2_actual <= 1.118:
		ppc_master_obj.v2_counter = 0
		ppc_master_obj.v2_shutdown = 0 # Running
	elif 0.85 <= ppc_master_obj.v2_actual < 0.90:
		ppc_master_obj.v2_counter += 1
		ppc_master_obj.v2_shutdown = 2 # Stopping
	elif 1.118 < ppc_master_obj.v2_actual <= 1.15:
		ppc_master_obj.v2_counter += 1
		ppc_master_obj.v2_shutdown = 2 # Stopping
	elif ppc_master_obj.v2_actual < 0.85 or ppc_master_obj.v2_actual > 1.15:
		ppc_master_obj.v2_shutdown = 1 # Not Running

	# Voltage ranges phase 3
	if 0.90 <= ppc_master_obj.v3_actual <= 1.118:
		ppc_master_obj.v3_counter = 0
		ppc_master_obj.v3_shutdown = 0 # Running
	elif 0.85 <= ppc_master_obj.v3_actual < 0.90:
		ppc_master_obj.v3_counter += 1
		ppc_master_obj.v3_shutdown = 2 # Stopping
	elif 1.118 < ppc_master_obj.v3_actual <= 1.15:
		ppc_master_obj.v3_counter += 1
		ppc_master_obj.v3_shutdown = 2 # Stopping
	elif ppc_master_obj.v3_actual < 0.85 or ppc_master_obj.v3_actual > 1.15:
		ppc_master_obj.v3_shutdown = 1 # Not Running

# Check if frequency and voltage are within limits
def operating_ranges(ppc_master_obj, window_obj):
	
	if (ppc_master_obj.release):
		# Check limits for normal operation
		normal_op_limits(ppc_master_obj, window_obj)
		
		# Check counters for timeouts
		if ppc_master_obj.f_counter > f_timer:
			window_obj.ax2.set_title("Frequency shutdown timeout")
			ppc_master_obj.f_shutdown = 1 # Timeout = PPC Not Running
		if ppc_master_obj.v_counter > v_timer:
			window_obj.ax4.set_title("Voltage shutdown timeout")
			ppc_master_obj.v_shutdown = 1 # Timeout = PPC Not Running
		if ppc_master_obj.v2_counter > v_timer:
			window_obj.ax4.set_title("Voltage shutdown timeout")
			ppc_master_obj.v2_shutdown = 1 # Timeout = PPC Not Running
		if ppc_master_obj.v3_counter > v_timer:
			window_obj.ax4.set_title("Voltage shutdown timeout")
			ppc_master_obj.v3_shutdown = 1 # Timeout = PPC Not Running
		
		# If either f or v has gone out of range
		if (ppc_master_obj.f_shutdown == 1 or ppc_master_obj.v_shutdown == 1 or ppc_master_obj.v2_shutdown == 1 or ppc_master_obj.v3_shutdown == 1):
			ppc_master_obj.operational_state = 1
			ppc_master_obj.release = True
		# If you reach here it means that both f and v are still in range
		elif (ppc_master_obj.f_shutdown == 2 or ppc_master_obj.v_shutdown == 2 or ppc_master_obj.v2_shutdown == 2 or ppc_master_obj.v3_shutdown == 2):
			ppc_master_obj.operational_state = 2
		# No problem with f and v -> prioritize start/stop SCADA button
		else: 
			window_obj.ax2.set_title("Frequency ok")
			if ppc_master_obj.start_stop == 1 or ppc_master_obj.auto_start_state == 1:
				ppc_master_obj.operational_state = 0

	# Reconnection process
	else:
		# Frequency ranges
		if 49.9 <= ppc_master_obj.f_actual <= 50.1 and ppc_master_obj.v_actual >= 0.95 and ppc_master_obj.v2_actual >= 0.95 and ppc_master_obj.v3_actual >= 0.95:
			if ppc_master_obj.release_counter >= release_timer:
				ppc_master_obj.release = True
				ppc_master_obj.release_counter = 0
				ppc_master_obj.set_start_zero()
			else:
				ppc_master_obj.release_counter += 1
				window_obj.ax2.set_title(u"Enable in {}".format(release_timer-ppc_master_obj.release_counter))
		else:
			ppc_master_obj.release_counter = 0
			ppc_master_obj.release = False # Not Running					
	
	# print(ppc_master_obj.operational_state)	

# Check if internal P and Q setpoints are within limits
def limit(p_in_sp, q_in_sp, ppc_master_obj):
	# Check if p setpoint lays within limits
	if p_in_sp >= ppc_master_obj.max_P_cap:	p_lim = ppc_master_obj.max_P_cap
	elif p_in_sp <= 0: p_lim = 0
	else: p_lim = p_in_sp
        
	# Check U-Q curve
	q_lim = UQ_limit(q_in_sp, ppc_master_obj.v_actual)
	# Check P-Q curve
	q_lim2 = PQ_limit(q_lim, ppc_master_obj.p_actual_hv)
    
	return p_lim, q_lim2

def UQ_limit(q_in_sp, v_actual):

	q_lim_sp = 0
	# Upper half
	A = [0.0, 1.1]
	B = [0.2, 1.0]
	ab = (B[0]-A[0])/(B[1]-A[1])
    
	# Lower half
	D = [-0.35, 1.0]
	E = [0.0, 0.9]
	de = (E[0]-D[0])/(E[1]-D[1])

	if v_actual > 1.0:
		c = A[0] + ab*(v_actual-A[1])
		if (q_in_sp > c):
			# print(f'intersection = [{round(c, 3)}, {v_actual}]')
			q_lim_sp = c
		elif (q_in_sp < D[0]):
			# print(f'intersection = [{D[0]}, {v_actual}]')
			q_lim_sp = D[0]
		else:
			q_lim_sp = q_in_sp
	else:
		f = D[0] + de*(v_actual-D[1])
		if (q_in_sp < f):
			# print(f'intersection = [{round(f, 3)}, {v_actual}]')
			q_lim_sp = f
		elif (q_in_sp > B[0]):
			# print(f'intersection = [{B[0]}, {v_actual}]')
			q_lim_sp = B[0]
		else:
			q_lim_sp = q_in_sp

	# print(f'q_lim_sp = {q_lim_sp}')

	return q_lim_sp

def PQ_limit(q_in_sp, p_actual_hv):

	q_lim_sp = 0
	A = [-0.35, 0.2]
	B = [0.0, 0.0]
	C = [0.2, 0.2]
	ab = (B[0]-A[0])/(B[1]-A[1])
	bc = (C[0]-B[0])/(C[1]-B[1])

	if p_actual_hv < A[1]:
		if q_in_sp < 0:
			d = A[0] + ab*(p_actual_hv-A[1])
			if (q_in_sp < d):
				# print(f'intersection = [{round(d, 3)}, {p_actual_hv}]')
				q_lim_sp = d
			else:
				q_lim_sp = q_in_sp
		else:
			e = B[0] + bc*(p_actual_hv-B[1])
			if (q_in_sp > e):
				# print(f'intersection = [{round(e, 3)}, {p_actual_hv}]')
				q_lim_sp = e
			else:
				q_lim_sp = q_in_sp
	else:
		if q_in_sp < A[0]: q_lim_sp = A[0]
		elif q_in_sp > C[0]: q_lim_sp = C[0]
		else: q_lim_sp = q_in_sp
        
	# print(f'q_lim_sp = {q_lim_sp}')
    
	return q_lim_sp
