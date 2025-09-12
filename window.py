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
        self.ax2.set_ylim(47.5, 52.5)
        self.ax3.set_xlim(0, xmax)
        self.ax3.set_ylim(-0.6, 0.4)
        self.ax4.set_xlim(0, xmax)
        self.ax4.set_ylim(0.85, 1.15)
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
        self.ln12, = self.ax1.plot([], [], "r-", label='ex_sp')
        self.ln13, = self.ax1.plot([], [], "g-", label='in_sp')
        self.ax1.legend(handles=[self.ln11, self.ln12, self.ln13])
        # F plot
        self.ln21, = self.ax2.plot([], [], "b-", label="Actual")
        self.ln22, = self.ax2.plot([], [], "r--", label="49Hz")
        self.ln23, = self.ax2.plot([], [], "r--", label="51Hz")
        # Q plots
        self.ln31, = self.ax3.plot([], [], "b-", label="Actual")
        self.ln32, = self.ax3.plot([], [], "r-", label='ex_sp')
        self.ln33, = self.ax3.plot([], [], "g-", label='in_sp')
        self.ax3.legend(handles=[self.ln31, self.ln32, self.ln33])
        # V plot
        self.ln41, = self.ax4.plot([], [], "b-", label="Actual")
        self.ln42, = self.ax4.plot([], [], "r--", label="0.9pu")
        self.ln43, = self.ax4.plot([], [], "r--", label="1.18pu")
        # U-Q
        # self.ln51, = self.ax5.plot([], [], "b-", label="Actual")
        # self.ln52, = self.ax5.plot([], [], "g-", label="Setpoint")
        self.ln51, = self.ax5.plot([], [], "r-", label="Limit")
        self.ln52, = self.ax5.plot([], [], "w-", label="Actual", marker='o', mec='b')
        self.ln53, = self.ax5.plot([], [], "w-", label="Setpoint", marker='o', mec='g')
        self.ax5.legend(handles=[self.ln51, self.ln52, self.ln53])
        # P-Q
        # self.ln61, = self.ax6.plot([], [], "b-", label="Actual")
        # self.ln62, = self.ax6.plot([], [], "g-", label="Setpoint")
        self.ln61, = self.ax6.plot([], [], "r-", label="Limit")
        self.ln62, = self.ax6.plot([], [], "k-", label="Q(P)")
        self.ln63, = self.ax6.plot([], [], "w-", label="Actual", marker='o', mec='b')
        self.ln64, = self.ax6.plot([], [], "w-", label="Setpoint", marker='o', mec='g')
        # Q(U)
        self.ln71, = self.ax7.plot([], [], "r-", label="V control")
        self.ln72, = self.ax7.plot([], [], "g-", label="Q(U) w/limit")
        self.ln73, = self.ax7.plot([], [], "w-", label="Actual", marker='o', mec='b')
        self.ax7.legend(handles=[self.ln71, self.ln72])
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
    
    p_data = deque([], maxlen=smax)
    p_sp_data = deque([], maxlen=smax)
    p_nsp_data = deque([], maxlen=smax)
    f_data = deque([], maxlen=smax)
    f_up = deque([], maxlen=smax)
    f_dn = deque([], maxlen=smax)
    q_data = deque([], maxlen=smax)
    q_sp_data = deque([], maxlen=smax)
    q_nsp_data = deque([], maxlen=smax)
    v_data = deque([], maxlen=smax)
    v_up = deque([], maxlen=smax)
    v_dn = deque([], maxlen=smax)
    x_data = deque([], maxlen=smax)

    def plot_data(self, x, ppc_master_obj):
        self.x_data.append(x)
        # P plot
        self.p_data.append(ppc_master_obj.p_actual_hv)
        self.p_sp_data.append(ppc_master_obj.p_ex_sp)
        self.p_nsp_data.append(ppc_master_obj.p_in_sp)
        # F plot
        self.f_data.append(ppc_master_obj.f_actual)
        self.f_up.append(51)
        self.f_dn.append(49)
        # Q plots
        self.q_data.append(ppc_master_obj.q_actual_hv)
        self.q_sp_data.append(ppc_master_obj.q_ex_sp)
        self.q_nsp_data.append(ppc_master_obj.q_in_sp)
        # V plots
        self.v_data.append(ppc_master_obj.v_actual)
        self.v_up.append(1.118)
        self.v_dn.append(0.9)

        # Plot stuff
        # P plot
        self.ln11.set_data(self.x_data, self.p_data)
        self.ln12.set_data(self.x_data, self.p_sp_data)
        self.ln13.set_data(self.x_data, self.p_nsp_data)
        # F plot
        self.ln21.set_data(self.x_data, self.f_data)
        self.ln22.set_data(self.x_data, self.f_up)
        self.ln23.set_data(self.x_data, self.f_dn)
        # Q plot
        self.ln31.set_data(self.x_data, self.q_data)
        self.ln32.set_data(self.x_data, self.q_sp_data)
        self.ln33.set_data(self.x_data, self.q_nsp_data)
        # V plot
        self.ln41.set_data(self.x_data, self.v_data)
        self.ln42.set_data(self.x_data, self.v_up)
        self.ln43.set_data(self.x_data, self.v_dn)
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
        self.ln73.set_data(ppc_master_obj.v_actual, ppc_master_obj.q_actual_hv)
        # P-f
        self.ln82.set_data(ppc_master_obj.f_actual, ppc_master_obj.p_in_sp)
        self.ln83.set_data(ppc_master_obj.f_actual, ppc_master_obj.p_actual_hv)

        # Slide window
        if x>=xmax:
            self.ln11.axes.set_xlim(x-xmax, x)
            self.ln12.axes.set_xlim(x-xmax, x)
            self.ln13.axes.set_xlim(x-xmax, x)
            self.ln21.axes.set_xlim(x-xmax, x)
            self.ln31.axes.set_xlim(x-xmax, x)
            self.ln32.axes.set_xlim(x-xmax, x)
            self.ln41.axes.set_xlim(x-xmax, x)
        
        # Emulate FuncAnimation
        plt.pause(0.05) # 1/20Hz = 0.05 s (TG3, section 6.1.1, p.132)
    
    def plot_PF_curve(self, ppc_master_obj):
        # P(f) curve (limits fixed / slopes modifiable)
        s = ppc_master_obj.s_sp
        s_LFSMO = ppc_master_obj.s_LFSM_O
        s_LFSMU = ppc_master_obj.s_LFSM_U
        # Toggle setpoints
        if ppc_master_obj.local_remote == 0: p_ref = ppc_master_obj.local_P_sp
        else: p_ref = ppc_master_obj.remote_P_sp
        # p_ref = ppc_master_obj.p_ex_sp
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
        s = ppc_master_obj.slope_sp
        # Toggle setpoints
        if ppc_master_obj.local_remote == 0: v_ref = ppc_master_obj.local_V_sp
        else: v_ref = ppc_master_obj.remote_V_sp
        # v_ref = 1
        q_ref = 0
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
                    0,
                    0,
                    q_max,
                    q_max]
        self.ln71.set_data(v_vector, q_vector)
    
    def plot_QU_limit_curve(self, ppc_master_obj):
        # Q(U) with limit curve (can be modified through the config tool)
        # Toggle setpoints
        if ppc_master_obj.local_remote == 0: q_ref = ppc_master_obj.local_Q_sp
        else: q_ref = ppc_master_obj.remote_Q_sp
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
    
    def plot_QP_curve(self, ppc_master_obj):
        p_vector = []
        q_vector = []
    #     q_vector = [0, 0, 0.025, 0.025, 0.08, 0.1, 0.1, 0.12, 0.15, 0.16, 0.2, 0.2]
    #     p_vector = [0, 0.1, 0.15, 0.2, 0.25, 0.5, 0.66, 0.75, 0.75, 0.9, 0.95, 1.0]
        # Q(P) curve (can be modified through the config)
        for i in range(ppc_master_obj.numOfPoints):
            p_vector.append(float(ppc_master_obj.P_points[i]))
            q_vector.append(float(ppc_master_obj.Q_points[i]))
            
        # print(p_vector)
        # print(q_vector)
        self.ln62.set_data(q_vector, p_vector)