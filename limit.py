f_counter = 0
v_counter = 0
shutdown = False

# Check if frequency and voltage are within limits
def operating_ranges(ppc_master_obj, window_obj):
	global f_counter, v_counter, shutdown

	if shutdown:
        	pass
	else:
		# Frequency ranges
		if 49.0 <= ppc_master_obj.f_actual <= 51.0:
			window_obj.ax2.set_title("Frequency")
			f_counter = 0
			ppc_master_obj.f_shutdown = 0 # Runninlng
		elif 47.5 <= ppc_master_obj.f_actual < 49.0:
			window_obj.ax2.set_title(u"Underfrequency: shutdown in {}".format(1800-f_counter))
			f_counter += 1
			ppc_master_obj.f_shutdown = 2 # Stopping
		elif 51.0 < ppc_master_obj.f_actual <= 51.5:
			window_obj.ax2.set_title(u"Overfrequency: shutdown in {}".format(1800-f_counter))
			f_counter += 1
			ppc_master_obj.f_shutdown = 2 # Stopping
		elif ppc_master_obj.f_actual < 47.5 or ppc_master_obj.f_actual > 51.5:
			window_obj.ax2.set_title('Frequency out of range!')
			print("Frequency out of range - emergency shutdown")
			shutdown = True
			ppc_master_obj.f_shutdown = 1 # Not Running
        
		if ppc_master_obj.f_actual < 49.8 or ppc_master_obj.f_actual > 50.2:
			ppc_master_obj.p_mode = 1

		# Voltage ranges
		if 0.90 <= ppc_master_obj.v_actual <= 1.118:
			window_obj.ax4.set_title('Voltage')
			v_counter = 0
			ppc_master_obj.v_shutdown = 0 # Runninng
		elif 0.85 <= ppc_master_obj.v_actual < 0.90:
			window_obj.ax4.set_title(u"Undervoltage: shutdown in {}".format(3600-v_counter))
			v_counter += 1
			ppc_master_obj.v_shutdown = 2 # Stopping
		elif 1.118 < ppc_master_obj.v_actual <= 1.15:
			window_obj.ax4.set_title(u"Overvoltage: shutdown in {}".format(3600-v_counter))
			v_counter += 1
			ppc_master_obj.v_shutdown = 2 # Stopping
		elif ppc_master_obj.v_actual < 0.85 or ppc_master_obj.v_actual > 1.15:
			window_obj.ax4.set_title('Voltage out of range!')
			print("Voltage out of range - emergency shutdown")
			shutdown = True
			ppc_master_obj.v_shutdown = 1 # Not Running
        
		if f_counter > 1800:
			window_obj.ax2.set_title("Frequency shutdown timeout")
			print("Frequency shutdown timeout")
			shutdown = True
			ppc_master_obj.f_shutdown = 1 # Not Running
        
		if v_counter > 3600:
			window_obj.ax4.set_title("Voltage shutdown timeout")
			print("Voltage shutdown timeout")
			shutdown = True
			ppc_master_obj.v_shutdown = 1 # Not Running
        
	return shutdown

# Check if internal P and Q setpoints are within limits
def limit(p_in_sp, q_in_sp, ppc_master_obj):

	# Check if p setpoint lays within limits
	if p_in_sp >= ppc_master_obj.max_P_cap:
		p_lim = ppc_master_obj.max_P_cap
	elif p_in_sp <= 0:
		p_lim = 0
	else:
		p_lim = p_in_sp
        
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
