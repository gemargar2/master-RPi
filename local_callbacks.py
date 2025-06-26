import json

# Local setpoints

def local_P_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.local_P_sp = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["local_P_sp"] = var
    # Update plots
    window_obj.plot_PF_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_Q_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.local_Q_sp = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["local_Q_sp"] = var
    # Update plots
    window_obj.plot_QU_limit_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_PF_setpoint(ppc_master_obj, var):
    ppc_master_obj.local_PF_sp = var
    ppc_master_obj.memory["local_PF_sp"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_V_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.local_V_sp = var/ppc_master_obj.V_nom
    ppc_master_obj.memory["local_V_sp"] = var
    # Update plots
    window_obj.plot_QU_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

# Universal setpoints

def local_s_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.s_sp = var/100
    ppc_master_obj.memory["s_sp"] = var/100
    # Update plots
    window_obj.plot_PF_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_s_LFSM_O_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.s_LFSM_O = var/100
    ppc_master_obj.memory["s_LFSM_O"] = var/100
    # Update plots
    window_obj.plot_PF_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_s_LFSM_U_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.s_LFSM_U = var/100
    ppc_master_obj.memory["s_LFSM_U"] = var/100
    # Update plots
    window_obj.plot_PF_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_slope_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.slope_sp = var/100
    ppc_master_obj.memory["slope_sp"] = var/100
    # Update plots
    window_obj.plot_QU_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_V_deadband_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.V_deadband_sp = var/100
    ppc_master_obj.memory["V_deadband_sp"] = var/100
    # Update plots
    window_obj.plot_QU_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

# Gradients

def local_P_gradient_setpoint(ppc_master_obj, var):
    ppc_master_obj.P_grad = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["P_grad"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_F_gradient_setpoint(ppc_master_obj, var):
    ppc_master_obj.F_grad = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["F_grad"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_MPPT_gradient_setpoint(ppc_master_obj, var):
    ppc_master_obj.MPPT_grad = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["MPPT_grad"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

# Active Power PID params

def local_P_Kp(ppc_master_obj, var):
    ppc_master_obj.p_kp = var
    ppc_master_obj.memory["p_kp"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_P_Ki(ppc_master_obj, var):
    ppc_master_obj.p_ki = var
    ppc_master_obj.memory["p_ki"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_P_Kd(ppc_master_obj, var):
    ppc_master_obj.p_kd = var
    ppc_master_obj.memory["p_kd"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_P_dt(ppc_master_obj, var):
    ppc_master_obj.p_dt = var
    ppc_master_obj.memory["p_dt"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

# Rective Power PID params

def local_Q_Kp(ppc_master_obj, var):
    ppc_master_obj.q_kp = var
    ppc_master_obj.memory["q_kp"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_Q_Ki(ppc_master_obj, var):
    ppc_master_obj.q_ki = var
    ppc_master_obj.memory["q_ki"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_Q_Kd(ppc_master_obj, var):
    ppc_master_obj.q_kd = var
    ppc_master_obj.memory["q_kd"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def local_Q_dt(ppc_master_obj, var):
    ppc_master_obj.q_dt = var
    ppc_master_obj.memory["q_dt"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)