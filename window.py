import matplotlib.pyplot as plt

xmax = 30 # seconds

class Window_class:

	def __init__(self):
		# --- init plot --------------
		# Landscape
		self.fig = plt.figure(figsize=(18, 8))
		#self.fig = plt.figure(figsize=(12, 8))
		mngr = plt.get_current_fig_manager()
		mngr.window.geometry("+50+100")
		self.fig.suptitle('Master PPC: Local')

		# create axis
		self.ax1 = self.fig.add_subplot(241)
		self.ax2 = self.fig.add_subplot(242)
		self.ax3 = self.fig.add_subplot(245)
		self.ax4 = self.fig.add_subplot(246)
		self.ax5 = self.fig.add_subplot(248)
		self.ax6 = self.fig.add_subplot(244)
		self.ax7 = self.fig.add_subplot(247)
		self.ax8 = self.fig.add_subplot(243)

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
		self.ax3.set_ylim(-0.8, 0.8)
		self.ax4.set_xlim(0, xmax)
		self.ax4.set_ylim(0.8, 1.2)
		self.ax5.set_xlim(-0.4, 0.5)
		self.ax5.set_ylim(0.85, 1.18)
		self.ax6.set_xlim(-0.4, 0.5)
		self.ax6.set_ylim(-0.1, 1.15)
		self.ax7.set_xlim(0.85, 1.15)
		self.ax7.set_ylim(-0.4, 0.4)
		self.ax8.set_xlim(49.6, 50.4)
		self.ax8.set_ylim(0.1, 0.9)

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
		self.ln36, = self.ax3.plot([], [], "k-", label='pid_sp')
		self.ln37, = self.ax3.plot([], [], "g-", label='grad_sp')
		self.ax3.legend(handles=[self.ln31, self.ln32, self.ln33, self.ln34, self.ln35, self.ln36, self.ln37])
		# V plot
		self.ln41, = self.ax4.plot([], [], "b-", label="vab")
		self.ln42, = self.ax4.plot([], [], "g-", label="vbc")
		self.ln43, = self.ax4.plot([], [], "m-", label="vca")
		self.ln44, = self.ax4.plot([], [], "r--", label="0.9pu")
		self.ln45, = self.ax4.plot([], [], "r--", label="1.118pu")
		self.ln46, = self.ax4.plot([], [], "k--", label="0.85pu")
		self.ln47, = self.ax4.plot([], [], "k--", label="1.15pu")
		self.ax4.legend(handles=[self.ln41, self.ln42, self.ln43])
		# U-Q
		self.ln51, = self.ax5.plot([], [], "r-", label="IPTO Limit")
		self.ln52, = self.ax5.plot([], [], "g-", label="VDE opt.2")
		self.ln53, = self.ax5.plot([], [], "w-", label="Setpoint", marker='o', mec='k')
		self.ax5.legend(handles=[self.ln51, self.ln52, self.ln53])
		# P-Q
		self.ln61, = self.ax6.plot([], [], "r-", label="IPTO Limit")
		self.ln62, = self.ax6.plot([], [], "g-", label="VDE opt.2")
		self.ln63, = self.ax6.plot([], [], "b-", label="Q(P)")
		self.ln64, = self.ax6.plot([], [], "w-", label="Setpoint", marker='o', mec='k')
		self.ax6.legend(handles=[self.ln61, self.ln62, self.ln63, self.ln64])
		# Q(U)
		self.ln71, = self.ax7.plot([], [], "r-", label="Q(U)")
		self.ln72, = self.ax7.plot([], [], "g-", label="Q(U) w/limit")
		self.ln73, = self.ax7.plot([], [], "b-", label="V control")
		self.ln74, = self.ax7.plot([], [], "w-", label="Setpoint", marker='o', mec='k')
		self.ax7.legend(handles=[self.ln71, self.ln72, self.ln73, self.ln74])
		# P(f)
		self.ln81, = self.ax8.plot([], [], "g-", label="LFSM")
		self.ln82, = self.ax8.plot([], [], "r-", label="FSM")
		self.ln83, = self.ax8.plot([], [], "w-", label="Setpoint", marker='o', mec='k')
		self.ax8.legend(handles=[self.ln81, self.ln82, self.ln83])

		# V-Q limits IPTO (fixed)
		q_vector = [-0.35, 0, 0.2, 0.2, 0, -0.35, -0.35]
		v_vector = [1.1, 1.1, 1, 0.9, 0.9, 1, 1.1]
		self.ln51.set_data(q_vector, v_vector)
		
		# V-Q limits IPTO (fixed)
		q_vector = [0.41, 0.27, -0.33, -0.33, 0.08, 0.41, 0.41]
		v_vector = [0.875, 0.875, 1, 1.15, 1.15, 1.118, 0.875]
		self.ln52.set_data(q_vector, v_vector)

		# IPTO P-Q limits (fixed)
		q_vector = [0, -0.35, -0.35, 0.2, 0.2, 0]
		p_vector = [0, 0.2, 1, 1, 0.2, 0]
		self.ln61.set_data(q_vector, p_vector)
		
		# VDE P-Q limits (fixed)
		q_vector = [-0.1, -0.33, -0.33, 0.41, 0.41, 0.1, -0.1]
		p_vector = [0.1, 0.2, 1, 1, 0.2, 0.1, 0.1]
		self.ln62.set_data(q_vector, p_vector)

		self.fig.tight_layout(pad=2.0)
		# self.fig.subplots_adjust(
		#     top=0.981,
		#     bottom=0.049,
		#     left=0.042,
		#     right=0.981,
		#     hspace=0.2,
		#     wspace=0.2
		# )
	
	# Plot data
	def plot_data(self, ppc_master_obj):
		x = ppc_master_obj.x
		# Update FSM Characteristic
		if ppc_master_obj.fsm_pref_flag: self.plot_FSM_curve(ppc_master_obj)
		if ppc_master_obj.lfsm_pref_flag: self.plot_LFSM_curve(ppc_master_obj)
		
		# Plot stuff
		# P plot
		self.ln11.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_actual_data)
		self.ln12.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_scada_sp)
		self.ln13.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_tso_sp)
		self.ln14.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_fose_sp)
		self.ln15.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_in_sp_data)
		self.ln16.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_grad_sp_data)
		self.ln17.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.p_pid_sp_data)
		# F plot
		self.ln21.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.f_data)
		self.ln22.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.f_up)
		self.ln23.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.f_dn)
		self.ln24.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.f_up2)
		self.ln25.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.f_dn2)
		# Q plot
		self.ln31.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_actual_data)
		self.ln32.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_scada_sp)
		self.ln33.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_tso_sp)
		self.ln34.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_fose_sp)
		self.ln35.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_in_sp_data)
		self.ln36.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_pid_sp_data)
		self.ln37.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.q_grad_sp_data)
		# V plot
		self.ln41.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.vab_data)
		self.ln42.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.vbc_data)
		self.ln43.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.vca_data)
		self.ln44.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.v_up)
		self.ln45.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.v_dn)
		self.ln46.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.v_up2)
		self.ln47.set_data(ppc_master_obj.plot_v.x_data, ppc_master_obj.plot_v.v_dn2)
		# V-Q
		self.ln53.set_data(ppc_master_obj.plot_v.q_in_sp, ppc_master_obj.plot_v.hv_meter.v_actual)
		# P-Q
		self.ln64.set_data(ppc_master_obj.plot_v.q_in_sp, ppc_master_obj.plot_v.p_in_sp)
		# Q_U characteristics
		self.ln74.set_data(ppc_master_obj.plot_v.hv_meter.v_actual, ppc_master_obj.plot_v.q_in_sp)
		# P-f
		self.ln83.set_data(ppc_master_obj.plot_v.hv_meter.f_actual, ppc_master_obj.plot_v.p_in_sp)

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
			self.ln37.axes.set_xlim(x-xmax, x)
			self.ln41.axes.set_xlim(x-xmax, x)
			self.ln42.axes.set_xlim(x-xmax, x)
			self.ln43.axes.set_xlim(x-xmax, x)
			self.ln44.axes.set_xlim(x-xmax, x)
			self.ln45.axes.set_xlim(x-xmax, x)
			self.ln46.axes.set_xlim(x-xmax, x)
			self.ln47.axes.set_xlim(x-xmax, x)
        
		# Emulate FuncAnimation
		plt.pause(1/ppc_master_obj.sampling_rate) # 1/20Hz = 0.05 s (TG3, section 6.1.1, p.132)
	
	def plot_FSM_curve(self, ppc_master_obj):
		# P(f) curve (limits fixed / slopes modifiable)
		s = ppc_master_obj.s_FSM
		# Toggle setpoints
		p_ref = ppc_master_obj.hv_meter.p_actual
		f_ref = 50
		f_vector = [47.5,
                	49.8,
                	49.99,
                	50.01,
                	50.2,
                	51.5]
		p_vector = [p_ref + 0.19/(s*f_ref),
                	p_ref + 0.19/(s*f_ref),
                	p_ref,
                	p_ref,
                	p_ref - 0.19/(s*f_ref),
                	p_ref - 0.19/(s*f_ref)]
                
		self.ln82.set_data(f_vector, p_vector)

	def plot_LFSM_curve(self, ppc_master_obj):
		p_ref = ppc_master_obj.hv_meter.p_actual
		f_vector = [47.5,
                	49.8,
                	50.2,
                	51.5]
                
		p_vector = [p_ref + 2.3*0.4,
                	p_ref,
                	p_ref,
                	p_ref - 1.3*0.4*p_ref]
                
		self.ln81.set_data(f_vector, p_vector)

	def plot_QU_curve(self, ppc_master_obj):
		# Q(U) curve (can be modified through the config tool)
		s = ppc_master_obj.QU_s
		v_ref = ppc_master_obj.ex_sp.V_sp
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
		q_ref = ppc_master_obj.ex_sp.Q_sp
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
		# v_ref = 1
		s = ppc_master_obj.slope_sp
		v_ref = ppc_master_obj.ex_sp.V_sp
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
		self.ln63.set_data(ppc_master_obj.Q_points, ppc_master_obj.P_points)
