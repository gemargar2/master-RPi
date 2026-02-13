from time import sleep, time
import threading

step_time = 10
recFlag = False

def recorder(obj, log_obj):
	global recFlag
	start_time = time()
	while recFlag:
		#start = time.time()
		log_obj.write_data(obj, start_time)
		#stop = time.time()
		#plot_time_elapsed = stop-startl
		#print(f'plot = {plot_time_elapsed}')
		sleep(0.1)
	print("Write complete")

def test_app(obj, log_obj, window_obj):
	global recFlag
	
	while True:
		# Reset park
		obj.ex_sp.P_sp = 0.75
		obj.ex_sp.Q_sp = 0.0
		obj.ex_sp.V_sp = 1.0
		obj.ex_sp.PF_sp = 1.0
		obj.p_mode = 0 # 0 = P control (PID) / 1 = F control (FSM) / 2 = P Open Loop / 3 = MPPT control
		obj.q_mode = 0 # 0 = Q control (PID) / 1 = Q(P) control / 2 = V control / 3 = PF control / 4 = Q Open Loop / 5 = Q(U) / 6 = Q(U) with limit	
		print("-------------- SETPOINT COMMANDS TEST MENU ------------------")
		print("Prerequisite: Comment out controller_core.py line 63")
		print("Test 00: Reactive power step response")
		print("Test 1: Displacement factor cos(phi) (6.1.3.2)")
		print("Test 3: Q(U) characteristic (6.1.3.4)")
		print("Test 4: Characteristic curve Q(P) (6.1.3.5)")
		print("Test 5: Active power P (6.1.3.6)")
		print("Test 6: Displacement factor cos(phi) (6.1.4.2)")
		print("Test 9: Characteristic curve Q(P) (6.1.4.5)")
		print("Test 10: Active power P (6.1.4.6)")
		print("Test 11: Determination of the Switchover Behaviour (6.1.5)")
		print("Test 16: Controller Bridging (Slave mode) (6.1.9)")
		print("Test 17: Prioritization of the Grid Operator Demand (6.1.10)")
		ans = input("Enter test code = ")
		if ans == '00':
			print("Test 00: Reactive power step response")
			log_obj.init_file()
			rec = threading.Thread(target = recorder, args=(obj, log_obj))
			recFlag = True
			rec.start()
			test00(obj)
			recFlag = False
			rec.join()
		elif ans == '1':
			print("Test 1: Displacement factor cos(phi) (6.1.3.2)")
			log_obj.init_file()
			rec = threading.Thread(target = recorder, args=(obj, log_obj))
			recFlag = True
			rec.start()
			test1(obj)
			recFlag = False
			rec.join()
		elif ans == '3':
			print("Test 3.2: Q(U) characteristic (6.1.3.4)")
			log_obj.init_file()
			rec = threading.Thread(target = recorder, args=(obj, log_obj))
			recFlag = True
			rec.start()
			test3(obj, window_obj)
			recFlag = False
			rec.join()
		elif ans == '4':
			print("Test 4: Characteristic curve Q(P) (6.1.3.5)")
			log_obj.init_file()
			rec = threading.Thread(target = recorder, args=(obj, log_obj))
			recFlag = True
			rec.start()
			test4(obj)
			recFlag = False
			rec.join()
		elif ans == '5':
			print("Test 5: Active power P (6.1.3.6)")
			test5(obj)
		elif ans == '6':
			print("Test 6: Displacement factor cos(phi) (6.1.4.2)")
			test6(obj)
		elif ans == '9':
			print("Test 9: Characteristic curve Q(P) (6.1.4.5)")
			test9(obj)
		elif ans == '10':
			print("Test 10: Active power P (6.1.4.6)")
			print("-------------- Subtest menu ------------------")
			print("Test 10a: P gradient = 0.66% Pn/s")
			print("Test 10b: P gradient = 0.33% Pn/s")
			print("Test 10c: P gradient = 4% Pn/min")
			ans = input("Enter subtest code = ")
			if ans == '10a':
				print("Test 10a: P gradient = 0.66% Pn/s")
				test10a(obj)
			elif ans == '10b':
				print("Test 10b: P gradient = 0.33% Pn/s")
				test10bc(obj)
			elif ans == '10c':
				print("Test 10c: P gradient = 4% Pn/min")
				test10bc(obj)
		elif ans == '11':
			print("Test 11: Determination of the Switchover Behaviour (6.1.5)")
			test11(obj)
		elif ans == '16':
			print("Test 16: Controller Bridging (Slave mode) (6.1.9)")
			pass
		elif ans == '17':
			print("Test 17: Prioritization of the Grid Operator Demand (6.1.10)")
			test17(obj)

def test00(obj):
	# Enter the correct mode
	obj.q_mode = 3 # 3 = PF control
	print("Step 2: PF = -0.975")
	obj.ex_sp.PF_sp = -0.95
	sleep(step_time)

def test1(obj):
	# Enter the correct mode
	obj.q_mode = 3 # 3 = PF control
	print("Step 1: PF = 1.0")
	obj.ex_sp.PF_sp = 1
	sleep(step_time)
	print("Step 2: PF = -0.975")
	obj.ex_sp.PF_sp = -0.975
	sleep(step_time)
	print("Step 3: PF = -0.95")
	obj.ex_sp.PF_sp = -0.95
	sleep(step_time)
	print("Step 4: PF = 1.0")
	obj.ex_sp.PF_sp = 1
	sleep(step_time)
	print("Step 5: PF = +0.975")
	obj.ex_sp.PF_sp = 0.975
	sleep(step_time)
	print("Step 6: PF = +0.95")
	obj.ex_sp.PF_sp = 0.95
	sleep(step_time)
	print("Step 7: PF = +0.99")
	obj.ex_sp.PF_sp = 0.99
	sleep(step_time)
	print("Finish: PF = 1.0")
	obj.ex_sp.PF_sp = 1

def test3(obj, window_obj):
	# Enter the correct mode
	obj.q_mode = 5 # 5 = Q(U) control
	print("Step 1: V = 1.0 p.u (150 kV)")
	obj.ex_sp.V_sp = 1
	window_obj.plot_QU_curve(obj)
	sleep(step_time)
	print("Step 2: V = 0.98 p.u (147 kV)")
	obj.ex_sp.V_sp = 0.98
	window_obj.plot_QU_curve(obj)
	sleep(step_time)
	print("Step 3: V = 1.02 p.u (153 kV)")
	obj.ex_sp.V_sp = 1.02
	window_obj.plot_QU_curve(obj)
	sleep(step_time)
	print("Finish: V = 1.0 p.u (150 kV)")
	obj.ex_sp.V_sp = 1
	window_obj.plot_QU_curve(obj)

def test4(obj):
	# Enter the correct mode
	obj.q_mode = 1 # 1 = Q(P) control
	print("Step 1: P = 0.90 p.u (19.98 MW) ")
	obj.ex_sp.P_sp = 0.9
	sleep(step_time)
	print("Step 2: P = 0.75 p.u (16.65 MW) ")
	obj.ex_sp.P_sp = 0.75
	sleep(step_time)
	print("Step 3: P = 0.60 p.u (13.32 MW) ")
	obj.ex_sp.P_sp = 0.6
	sleep(step_time)
	print("Step 4: P = 0.55 p.u (12.21 MW) ")
	obj.ex_sp.P_sp = 0.55
	sleep(step_time)
	print("Step 5: P = 0.50 p.u (11.1 MW) ")
	obj.ex_sp.P_sp = 0.5
	sleep(step_time)
	print("Step 6: P = 0.00 p.u (0.0 MW) ")
	obj.ex_sp.P_sp = 0
	sleep(step_time)

def test5(obj):
	# Enter the correct mode
	obj.p_mode = 0 # 0 = P control (PID)
	print("Step 1: P = 0.90 p.u (19.98 MW) ")
	obj.ex_sp.P_sp = 0.9
	sleep(step_time)
	print("Step 2: P = 0.60 p.u (13.32 MW) ")
	obj.ex_sp.P_sp = 0.6
	sleep(step_time)
	print("Step 3: P = 0.30 p.u (6.66 MW) ")
	obj.ex_sp.P_sp = 0.3
	sleep(step_time)
	print("Step 4: P = 0.00 p.u (0.0 MW) ")
	obj.ex_sp.P_sp = 0
	sleep(step_time)

def test6(obj):
	# Set the right setpoint
	obj.ex_sp.P_sp = 0.75
	# Enter the correct mode
	obj.q_mode = 3 # 3 = PF control
	print("Step 1: PF = 1.0")
	obj.ex_sp.PF_sp = 1
	sleep(step_time)
	print("Step 2: PF = -0.95")
	obj.ex_sp.PF_sp = -0.95
	sleep(step_time)
	print("Step 3: PF = +0.95")
	obj.ex_sp.PF_sp = 0.95
	sleep(step_time)
	print("Step 4: PF = 1.0")
	obj.ex_sp.PF_sp = 1
	sleep(step_time)

def test9(obj):
	# Enter the correct mode
	obj.q_mode = 1 # 1 = Q(P) control
	print("Step 1: P = 0.92 p.u (20.42 MW) ")
	obj.ex_sp.P_sp = 0.92
	sleep(step_time)
	print("Step 2: P = 0.30 p.u (6.66 MW) ")
	obj.ex_sp.P_sp = 0.3
	sleep(step_time)

def test10a(obj):
	# Enter the correct mode
	obj.p_mode = 0 # 0 = P control (PID)
	print("Step 1: P = 0.90 p.u (19.98 MW) ")
	obj.ex_sp.P_sp = 0.9
	sleep(step_time)
	print("Step 2: P = 0.00 p.u (0.0 MW) ")
	obj.ex_sp.P_sp = 0
	sleep(step_time)
	print("Step 3: P = 0.90 p.u (19.98 MW) ")
	obj.ex_sp.P_sp = 0.9
	sleep(step_time)

def test10bc(obj):
	# Enter the correct mode
	obj.p_mode = 0 # 0 = P control (PID)
	print("Step 1: P = 0.70 p.u (15.54 MW) ")
	obj.ex_sp.P_sp = 0.7
	sleep(step_time)
	print("Step 2: P = 0.50 p.u (11.1 MW) ")
	obj.ex_sp.P_sp = 0.5
	sleep(step_time)
	print("Step 3: P = 0.70 p.u (15.54 MW) ")
	obj.ex_sp.P_sp = 0.7
	sleep(step_time)

def test11(obj):
	# Set the right setpoints
	obj.ex_sp.P_sp = 0.75
	obj.ex_sp.Q_sp = 0
	obj.ex_sp.V_sp = 1.07
	# Enter the correct mode
	print("Step 1: Q(U) with limit Qref = 0.0")
	obj.q_mode = 6 # 6 = Q(U) with limit
	sleep(step_time)
	print("Step 2: Q(U) Vref = 1.07 p.u (160.5kV) ")
	obj.q_mode = 5 # 5 = Q(U)
	sleep(step_time)

def test17(obj):
	# Local = SCADA / Remote = TSO/FOSE
	obj.local_remote = 1 # 1 = Remote
	# Network Operator and 3rd party setpoints (TSO)
	print("Step 1: TSO=100% / FOSE=100%")
	obj.tso_P_sp = 1
	obj.fose_P_sp = 1
	sleep(step_time)
	print("Step 1: TSO=60% / FOSE=100%")
	obj.tso_P_sp = 0.6
	obj.fose_P_sp = 1
	sleep(step_time)
	print("Step 2: TSO=60% / FOSE=30%")
	obj.tso_P_sp = 0.6
	obj.fose_P_sp = 0.3
	sleep(step_time)
	print("Step 3: TSO=0% / FOSE=30%")
	obj.tso_P_sp = 0
	obj.fose_P_sp = 0.3
	sleep(step_time)
	
