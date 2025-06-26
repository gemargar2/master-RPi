import json

# Local setpoints

def remote_P_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.remote_P_sp = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["remote_P_sp"] = var
    # Update plots
    window_obj.plot_PF_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def remote_Q_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.remote_Q_sp = var/ppc_master_obj.S_nom
    ppc_master_obj.memory["remote_Q_sp"] = var
    # Update plots
    window_obj.plot_QU_limit_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def remote_PF_setpoint(ppc_master_obj, var):
    ppc_master_obj.remote_PF_sp = var
    ppc_master_obj.memory["remote_PF_sp"] = var
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)

def remote_V_setpoint(ppc_master_obj, window_obj, var):
    # Update ppc_master_obj variable
    ppc_master_obj.remote_V_sp = var/ppc_master_obj.V_nom
    ppc_master_obj.memory["remote_V_sp"] = var
    # Update plots
    window_obj.plot_QU_curve(ppc_master_obj)
    # Update setpoint json file
    with open("setpoints.json", "w") as outfile:
        json.dump(ppc_master_obj.memory, outfile)