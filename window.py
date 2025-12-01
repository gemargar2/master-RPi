import matplotlib.pyplot as plt
from collections import deque

xmax = 40 # seconds
smax = 400 # samples

class Window_class:

	def __init__(self):
		# --- init plot --------------
		# Landscape
		self.fig = plt.figure(figsize=(18, 8))
		mngr = plt.get_current_fig_manager()
		mngr.window.geometry("+50+100")
		self.fig.suptitle('Master PPC: Local')

		# create axis
		self.ax1 = self.fig.add_subplot(241)
		self.ax2 = self.fig.add_subplot(242)
		self.ax3 = self.fig.add_subplot(245)
		self.ax4 = self.fig.add_subplot(246)
		self.ax5 = self.fig.add_subplot(243)
		self.ax6 = self.fig.add_subplot(244)
		self.ax7 = self.fig.add_subplot(247)
		self.ax8 = self.fig.add_subplot(248)

		# Set titles of subplots
		self.ax1.set_title('Active Power')
		self.ax2.set_title('Frequency')
		self.ax3.set_title('Reactive Power')
		self.ax4.set_title('Voltage')
		self.ax5.set_title('U-Q')
		self.ax6.set_title('P-Q')
		self.ax7.set_title('Q(U)')
		self.ax8.set_title('P(f)')

		# set label names
		self.ax1.set_xlabel("t")
		self.ax1.set_ylabel("P (p.u)")
		self.ax2.set_xlabel("t")
		self.ax2.set_ylabel("f (Hz)")
		self.ax3.set_xlabel("t")
		self.ax3.set_ylabel("Q (p.u)")
		self.ax4.set_xlabel("t")
		self.ax4.set_ylabel("V (p.u)")
		self.ax5.set_xlabel("Q (p.u)")
		self.ax5.set_ylabel("V (p.u)")
		self.ax6.set_xlabel("Q (p.u)")
		self.ax6.set_ylabel("P (p.u)")
		self.ax7.set_xlabel("U (p.u)")
		self.ax7.set_ylabel("Q (p.u)")
		self.ax8.set_xlabel("f (Hz)")
		self.ax8.set_ylabel("P (p.u)")

		# enable grid
		self.ax1.grid(True)
		self.ax2.grid(True)
		self.ax3.grid(True)
		self.ax4.grid(True)
		self.ax5.grid(True)
		self.ax6.grid(True)
		self.ax7.grid(True)
		self.ax8.grid(True)

		# set axis limits
		self.ax1.set_xlim(0, xmax)
		self.ax1.set_ylim(-0.1, 1.1)
		self.ax2.set_xlim(0, xmax)
		self.ax2.set_ylim(46.5, 52.5)
		self.ax3.set_xlim(0, xmax)
		self.ax3.set_ylim(-0.6, 0.4)
		self.ax4.set_xlim(0, xmax)
		self.ax4.set_ylim(0.8, 1.2)
		self.ax5.set_xlim(-0.6, 0.4)
		self.ax5.set_ylim(0.85, 1.15)
		self.ax6.set_xlim(-0.6, 0.4)
		self.ax6.set_ylim(-0.1, 1.15)
		self.ax7.set_xlim(0.85, 1.15)
		self.ax7.set_ylim(-0.6, 0.4)
		self.ax8.set_xlim(49.6, 50.4)
		self.ax8.set_ylim(0.2, 0.8)
		# self.ax8.set_xlim(47.5, 51.5)
		# self.ax8.set_ylim(-0.1, 1.1)

		# P plot
		self.ln11, = self.ax1.plot([], [], "b-", label='Actual')
		self.ln12, = self.ax1.plot([], [], "m--", label='scada')
		self.ln13, = self.ax1.plot([], [], "c--", label='tso')
		self.ln14, = self.ax1.plot([], [], "y--", label='fose')
		self.ln15, = self.ax1.plot([], [], "r-", label='in_sp')
		self.ln16, = self.ax1.plot([], [], "g-", label='grad_sp')
		self.ln17, = self.ax1.plot([], [], "k-", label='pid_sp')
		self.ax1.legend(handles=[self.ln11, self.ln12, self.ln13, self.ln14, self.ln15, self.ln16, self.ln17])
		# F plot
		self.ln21, = self.ax2.plot([], [], "b-", label="Actual")
		self.ln22, = self.ax2.plot([], [], "r--", label="49Hz")
		self.ln23, = self.ax2.plot([], [], "r--", label="51Hz")
		self.ln24, = self.ax2.plot([], [], "k--", label="47.5Hz")
		self.ln25, = self.ax2.plot([], [], "k--", label="51.5Hz")
		# Q plots
		self.ln31, = self.ax3.plot([], [], "b-", label="Actual")
		self.ln32, = self.ax3.plot([], [], "m--", label='scada')
		self.ln33, = self.ax3.plot([], [], "c--", label='tso')
		self.ln34, = self.ax3.plot([], [], "y--", label='fose')
		self.ln35, = self.ax3.plot([], [], "r-", label='in_sp')
		self.ln36, = self.ax3.plot([], [], "g-", label='grad_sp')
		self.ln37, = self.ax1.plot([], [], "k-", label='pid_sp')
		self.ax3.legend(handles=[self.ln31, self.ln32, self.ln33, self.ln34, self.ln35, self.ln36, self.ln37])
		# V plot
		self.ln41, = self.ax4.plot([], [], "b-", label="ph1")
		self.ln41, = self.ax4.plot([], [], "g-", label="ph1")
		self.ln41, = self.ax4.plot([], [], "m-", label="ph1")
		self.ln42, = self.ax4.plot([], [], "r--", label="0.9pu")
		self.ln43, = self.ax4.plot([], [], "r--", label="1.118pu")
		self.ln44, = self.ax4.plot([], [], "k--", label="0.85pu")
		self.ln45, = self.ax4.plot([], [], "k--", label="1.15pu")
		# U-Q
		# self.ln51, = self.ax5.plot([], [], "b-", label="Actual")
		# self.ln52, = self.ax5.plot([], [], "g-", label="Setpoint")
		self.ln51, = self.ax5.plot([], [], "r-", label="Limit")
		self.ln52, = self.ax5.plot([], [], "w-", label="Actual", marker='o', mec='b')
		self.ln53, = self.ax5.plot([], [], "w-", label="Setpoint", marker='o', mec='g')
		self.ax5.legend(handles=[self.ln51, self.ln52, self.ln53])
		# P-Q
		# self.ln61, = self.ax6.plot([], [], "b-", label="Actual")
		# self.ln62, = self.ax6.plot([], [], "g-", label="Setpoint")l
		self.ln61, = self.ax6.plot([], [], "r-", label="Limit")
		self.ln62, = self.ax6.plot([], [], "k-", label="Q(P)")
		self.ln63, = self.ax6.plot([], [], "w-", label="Actual", marker='o', mec='b')
		self.ln64, = self.ax6.plot([], [], "w-", label="Setpoint", marker='o', mec='g')
		# Q(U)
		self.ln71, = self.ax7.plot([], [], "r-", label="Q(U)")
		self.ln72, = self.ax7.plot([], [], "g-", label="Q(U) w/limit")
		self.ln73, = self.ax7.plot([], [], "b-", label="V control")
		self.ln74, = self.ax7.plot([], [], "w-", label="Actual", marker='o', mec='k')
		self.ax7.legend(handles=[self.ln71, self.ln72, self.ln73])
		# P(f)
		self.ln81, = self.ax8.plot([], [], "r-", label="limit")
		self.ln82, = self.ax8.plot([], [], "w-", label="Setpoint", marker='o', mec='g')
		self.ln83, = self.ax8.plot([], [], "w-", label="Actual", marker='o', mec='b')
		self.ax8.legend(handles=[self.ln82, self.ln83])

		# V-Q limits (fixed)
		q_vector = [-0.35, 0, 0.2, 0.2, 0, -0.35, -0.35]
		v_vector = [1.1, 1.1, 1, 0.9, 0.9, 1, 1.1]
		self.ln51.set_data(q_vector, v_vector)

		# P-Q limits (fixed)
		q_vector = [0, -0.35, -0.35, 0.2, 0.2, 0]
		p_vector = [0, 0.2, 1, 1, 0.2, 0]
		self.ln61.set_data(q_vector, p_vector)

		self.fig.tight_layout(pad=2.0)
		# self.fig.subplots_adjust(
		#     top=0.981,
		#     bottom=0.049,
		#     left=0.042,
		#     right=0.981,
		#     hspace=0.2,
		#     wspace=0.2
		# )
	
	# Samples/timestamps
	x_data = deque([], maxlen=smax)
	
	# P remote setpoints
	p_scada_sp = deque([], maxlen=smax)
	p_tso_sp = deque([], maxlen=smax)
	p_fose_sp = deque([], maxlen=smax)
	# P internal setpoints
	p_in_sp_data = deque([], maxlen=smax)
	p_grad_sp_data = deque([], maxlen=smax)
	p_pid_sp_data = deque([], maxlen=smax)
	# P measurement
	p_actual_data = deque([], maxlen=smax)
	
	# F setpoint
	f_data = deque([], maxlen=smax)
	f_up = deque([], maxlen=smax)
	f_dn = deque([], maxlen=smax)
	f_up2 = deque([], maxlen=smax)
	f_dn2 = deque([], maxlen=smax)
	
	# Q remote setpoints
	q_scada_sp = deque([], maxlen=smax)
	q_tso_sp = deque([], maxlen=smax)
	q_fose_sp = deque([], maxlen=smax)
	# Q internal setpoints
	q_in_sp_data = deque([], maxlen=smax)
	q_grad_sp_data = deque([], maxlen=smax)
	q_pid_sp_data = deque([], maxlen=smax)
	# Q measurement
	q_actual_data = deque([], maxlen=smax)
	
	# V setpoint
	v_data = deque([], maxlen=smax)
	v_up = deque([], maxlen=smax)
	v_dn = deque([], maxlen=smax)
	v_up2 = deque([], maxlen=smax)
	v_dn2 = deque([], maxlen=smax)
	
	# Plot data
	def plot_data(self, x, ppc_master_obj):
		# samples/timestamp
		self.x_data.append(x)
		
		# ------ P plot -------
		# P remote setpoints
		self.p_scada_sp.append(ppc_master_obj.local_P_sp)
		self.p_tso_sp.append(ppc_master_obj.tso_P_sp)
		self.p_fose_sp.append(ppc_master_obj.fose_P_sp)
		# P internal setpoints
		self.p_in_sp_data.append(ppc_master_obj.p_in_sp)
		self.p_grad_sp_data.append(ppc_master_obj.p_grad_sp)
		self.p_pid_sp_data.append(ppc_master_obj.p_pid_sp)
		# P measurement
		self.p_actual_data.append(ppc_master_obj.p_actual_hv)
		
		# F plot
		self.f_data.append(ppc_master_obj.f_actual)
		self.f_up.append(51)
		self.f_dn.append(49)
		self.f_up2.append(51.5)
		self.f_dn2.append(47.5)
		
		# ------ Q plot -------
		# Q remote setpoints
		self.q_scada_sp.append(ppc_master_obj.local_Q_sp)
		self.q_tso_sp.append(ppc_master_obj.tso_Q_sp)
		self.q_fose_sp.append(ppc_master_obj.fose_Q_sp)
		# Q internal setpoints
		self.q_in_sp_data.append(ppc_master_obj.q_in_sp)
		self.q_grad_sp_data.append(ppc_master_obj.q_grad_sp)
		self.q_pid_sp_data.append(ppc_master_obj.q_pid_sp)
		# Q measurement
		self.q_actual_data.append(ppc_master_obj.q_actual_hv)
		
		# V plots
		self.v_data.append(ppc_master_obj.v_actual)
		self.v_up.append(1.118)
		self.v_dn.append(0.9)
		self.v_up2.append(1.15)
		self.v_dn2.append(0.85)

		# Plot stuff
		# P plot
		self.ln11.set_data(self.x_data, self.p_actual_data)
		self.ln12.set_data(self.x_data, self.p_scada_sp)
		self.ln13.set_data(self.x_data, self.p_tso_sp)
		self.ln14.set_data(self.x_data, self.p_fose_sp)
		self.ln15.set_data(self.x_data, self.p_in_sp_data)
		self.ln16.set_data(self.x_data, self.p_grad_sp_data)
		self.ln17.set_data(self.x_data, self.p_pid_sp_data)
		# F plot
		self.ln21.set_data(self.x_data, self.f_data)
		self.ln22.set_data(self.x_data, self.f_up)
		self.ln23.set_data(self.x_data, self.f_dn)
		self.ln24.set_data(self.x_data, self.f_up2)
		self.ln25.set_data(self.x_data, self.f_dn2)
		# Q plot
		self.ln31.set_data(self.x_data, self.q_actual_data)
		self.ln32.set_data(self.x_data, self.q_scada_sp)
		self.ln33.set_data(self.x_data, self.q_tso_sp)
		self.ln34.set_data(self.x_data, self.q_fose_sp)
		self.ln35.set_data(self.x_data, self.q_in_sp_data)
		self.ln36.set_data(self.x_data, self.q_grad_sp_data)
		self.ln37.set_data(self.x_data, self.p_pid_sp_data)
		# V plot
		self.ln41.set_data(self.x_data, self.v_data)
		self.ln42.set_data(self.x_data, self.v_up)
		self.ln43.set_data(self.x_data, self.v_dn)
		self.ln44.set_data(self.x_data, self.v_up2)
		self.ln45.set_data(self.x_data, self.v_dn2)
		# V-Q
		# self.ln51.set_data(self.q_data, self.v_data)
		# self.ln52.set_data(self.q_nsp_data, self.v_data)
		self.ln52.set_data(ppc_master_obj.q_actual_hv, ppc_master_obj.v_actual)
		self.ln53.set_data(ppc_master_obj.q_in_sp, ppc_master_obj.v_actual)
		# P-Q
		# self.ln61.set_data(self.q_data, self.p_data)
		# self.ln62.set_data(self.q_nsp_data, self.p_nsp_data)
		self.ln63.set_data(ppc_master_obj.q_actual_hv, ppc_master_obj.p_actual_hv)
		self.ln64.set_data(ppc_master_obj.q_in_sp, ppc_master_obj.p_in_sp)
		self.ln74.set_data(ppc_master_obj.v_actual, ppc_master_obj.q_actual_hv)
		# P-f
		self.ln82.set_data(ppc_master_obj.f_actual, ppc_master_obj.p_in_sp)
		self.ln83.set_data(ppc_master_obj.f_actual, ppc_master_obj.p_actual_hv)

		# Slide window
		if x>=xmax:
			self.ln11.axes.set_xlim(x-xmax, x)
			self.ln12.axes.set_xlim(x-xmax, x)
			self.ln13.axes.set_xlim(x-xmax, x)
			self.ln14.axes.set_xlim(x-xmax, x)
			self.ln15.axes.set_xlim(x-xmax, x)
			self.ln16.axes.set_xlim(x-xmax, x)
			self.ln21.axes.set_xlim(x-xmax, x)
			self.ln22.axes.set_xlim(x-xmax, x)
			self.ln23.axes.set_xlim(x-xmax, x)
			self.ln24.axes.set_xlim(x-xmax, x)
			self.ln25.axes.set_xlim(x-xmax, x)
			self.ln31.axes.set_xlim(x-xmax, x)
			self.ln32.axes.set_xlim(x-xmax, x)
			self.ln33.axes.set_xlim(x-xmax, x)
			self.ln34.axes.set_xlim(x-xmax, x)
			self.ln35.axes.set_xlim(x-xmax, x)
			self.ln36.axes.set_xlim(x-xmax, x)
			self.ln41.axes.set_xlim(x-xmax, x)
			self.ln42.axes.set_xlim(x-xmax, x)
			self.ln43.axes.set_xlim(x-xmax, x)
			self.ln44.axes.set_xlim(x-xmax, x)
			self.ln45.axes.set_xlim(x-xmax, x)
        
		# Emulate FuncAnimation
		plt.pause(1/ppc_master_obj.sampling_rate) # 1/20Hz = 0.05 s (TG3, section 6.1.1, p.132)
    
	def plot_PF_curve(self, ppc_master_obj):
		# P(f) curve (limits fixed / slopes modifiable)
		s = ppc_master_obj.s_FSM
		s_LFSMO = ppc_master_obj.s_LFSM_O
		s_LFSMU = ppc_master_obj.s_LFSM_U
		# Toggle setpoints
		p_ref = ppc_master_obj.PF_p
		f_ref = 50
		f_vector = [47.5,
                	49.8 - (1 - (p_ref + 0.19/(s*f_ref)))*f_ref*s_LFSMU,
                	49.8,
                	49.99,
                	50.01,
                	50.2,
                	50.2 + (1 - (p_ref + 0.19/(s*f_ref)))*f_ref*s_LFSMO,
                	51.5]
		p_vector = [1,
                	1,
                	p_ref + 0.19/(s*f_ref),
                	p_ref,
                	p_ref,
                	p_ref - 0.19/(s*f_ref),
                	0,
                	0]
		self.ln81.set_data(f_vector, p_vector)

	def plot_QU_curve(self, ppc_master_obj):
		# Q(U) curve (can be modified through the config tool)
		s = ppc_master_obj.QU_s
		v_ref = ppc_master_obj.QU_v
		q_ref = 0
		q_max = ppc_master_obj.max_Q_cap
		q_min = ppc_master_obj.min_Q_cap
		db = ppc_master_obj.QU_db
		v_vector = [1.15,
			v_ref + db + (q_ref - q_min)*s,
			v_ref + db,
			v_ref - db,
			v_ref - db - (q_max - q_ref)*s,
			0.85]
		q_vector = [q_min,
			q_min,
			0,
			0,
			q_max,
			q_max]
		self.ln71.set_data(v_vector, q_vector)
    
	def plot_QU_limit_curve(self, ppc_master_obj):
		# Q(U) with limit curve (can be modified through the config tool)
		q_ref = ppc_master_obj.QU_q
		q_max = ppc_master_obj.max_Q_cap
		q_min = ppc_master_obj.min_Q_cap
		# Deadband limits are affected by voltage setpoint
		dba = ppc_master_obj.P2[0] + q_ref / ppc_master_obj.ma
		dbb = ppc_master_obj.P3[0] + q_ref / ppc_master_obj.mb
		# Vectors
		v_vector = [1.15,
			ppc_master_obj.P4[0],
			dbb,
			dba,
			ppc_master_obj.P1[0],
			0.85]
		q_vector = [q_min,
			q_min,
			q_ref,
			q_ref,
			q_max,
			q_max]
		self.ln72.set_data(v_vector, q_vector)

	def plot_V_control_curve(self, ppc_master_obj):
		# Q(U) curve (can be modified through the config tool)
		s = ppc_master_obj.slope_sp
		# Toggle setpoints
		if ppc_master_obj.local_remote == 0: v_ref = ppc_master_obj.local_V_sp
		else: v_ref = ppc_master_obj.remote_V_sp
		# v_ref = 1
		q_ref = 0.0
		# other limits
		q_max = ppc_master_obj.max_Q_cap
		q_min = ppc_master_obj.min_Q_cap
		db = ppc_master_obj.V_deadband_sp
		v_vector = [1.15,
			v_ref + db + (q_ref - q_min)*s,
			v_ref + db,
			v_ref - db,
			v_ref - db - (q_max - q_ref)*s,
			0.85]
		q_vector = [q_min,
			q_min,
			q_ref,
			q_ref,
			q_max,
			q_max]
		self.ln73.set_data(v_vector, q_vector)
    
	def plot_QP_curve(self, ppc_master_obj):
		self.ln62.set_data(ppc_master_obj.Q_points, ppc_master_obj.P_points)
