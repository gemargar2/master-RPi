import zmq
from remote_callbacks import *
from local_callbacks import *

def tso_rx(ppc_master_obj, window_obj):
    # Real
    context_rx = zmq.Context()
    socket_rx = context_rx.socket(zmq.PULL)
    socket_rx.connect("tcp://127.0.0.1:13002")

    while True:
        # Wait for command
        message = socket_rx.recv_json()

        # Check for local / remote signal
        if message['origin'] == 'localPlatform':
            if message['value_name'] == 'Local_Remote':
                ppc_master_obj.local_remote = int(message['value'])
                # Update plots
                window_obj.plot_PF_curve(ppc_master_obj)
                window_obj.plot_QU_curve(ppc_master_obj)
                window_obj.plot_QU_limit_curve(ppc_master_obj)
        
        if ppc_master_obj.local_remote == 0:
            if message['origin'] == 'TSO':
                # print("You are in local mode - TSO messages are ignored")
                pass
            # Local mode - only SCADA commands are taken into account   
            if message['origin'] == 'localPlatform':
                # ----------------------------- mode selection ------------------------------------------------------------
                if message['value_name'] == 'active_control_mode': ppc_master_obj.p_mode = int(message['value'])
                elif message['value_name'] == 'reactive_control_mode': ppc_master_obj.q_mode = int(message['value'])
                # ----------------------------- Local setpoint values  ------------------------------------------------------------
                elif message['value_name'] == 'P_setpoint': local_P_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'Q_setpoint': local_Q_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'PF_setpoint': local_PF_setpoint(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'V_setpoint': local_V_setpoint(ppc_master_obj, window_obj, float(message['value']))
                # ----------------------------- Universal setpoint values  ------------------------------------------------------------
                elif message['value_name'] == 's_setpoint': local_s_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 's_LFSM_O_setpoint': local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 's_LFSM-U_setpoint': local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'slope_setpoint': local_slope_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'V_deadband_setpoint': local_V_deadband_setpoint(ppc_master_obj, window_obj, float(message['value']))
                # ----------------------------- Gradient values -------------------------------------------------------------
                elif message['value_name'] == 'P_control_gradient': local_P_gradient_setpoint(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'F_control_gradient': local_F_gradient_setpoint(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'MPPT_control_gradient': local_MPPT_gradient_setpoint(ppc_master_obj, float(message['value']))
                # ----------------------------- P control PID parameter values ---------------------------------
                elif message['value_name'] == 'Kp_Pcontrol': local_P_Kp(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Ki_Pcontrol': local_P_Ki(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Kd_Pcontrol': local_P_Kd(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Ti_Pcontrol': local_P_dt(ppc_master_obj, float(message['value']))
                # ----------------------------- P control PID parameter values ---------------------------------
                elif message['value_name'] == 'Kp_Qcontrol': local_Q_Kp(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Ki_Qcontrol': local_Q_Ki(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Kd_Qcontrol': local_Q_Kd(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'Ti_Qcontrol': local_Q_dt(ppc_master_obj, float(message['value']))
                # ----------------------------- Controls -------------------------------------------------------------------
                elif message['value_name'] == 'Stop': ppc_master_obj.operational_state = 1
                elif message['value_name'] == 'Start': ppc_master_obj.operational_state = 0
                elif message['value_name'] == 'Auto_Start_command': ppc_master_obj.auto_start_state = int(message['value'])
                # ----------------------------- Simulation mode ------------------------------------------------------------
                elif message['value_name'] == 'Simulation_mode_command': ppc_master_obj.simulation_mode = int(message['value'])
                elif message['value_name'] == 'simulation_run_stop': ppc_master_obj.run_simulation(int(message['value']))
                elif message['value_name'] == 'voltage_disturbance': ppc_master_obj.v_disturbance = float(message['value'])
                elif message['value_name'] == 'frequency_disturbance': ppc_master_obj.f_disturbance = float(message['value'])
                elif message['value_name'] == 'simulation_duration': ppc_master_obj.simulation_duration = int(float(message['value']))
        
        # Remote mode - only TSO commands are taken into account - SCADA can still change mode to local
        elif ppc_master_obj.local_remote == 1:
            if message['origin'] == 'TSO':
                # ----------------------------- Local setpoint values  ------------------------------------------------------------
                if message['value_name'] == 'P_setpoint_remote': remote_P_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'Q_setpoint_remote': remote_Q_setpoint(ppc_master_obj, window_obj, float(message['value']))
                elif message['value_name'] == 'PF_setpoint_remote': remote_PF_setpoint(ppc_master_obj, float(message['value']))
                elif message['value_name'] == 'V_setpoint_remote': remote_V_setpoint(ppc_master_obj, window_obj, float(message['value']))
        
