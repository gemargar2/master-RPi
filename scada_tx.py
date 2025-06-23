from header import *
import math
import json

# --- MV quantities -------------------------------------------

def send_MV_quantities(ppc_master_obj):
    var1 = ppc_master_obj.p_actual_mv*ppc_master_obj.S_nom
    message1 = { "destination": "localPlatform", "value_name": "active_power_MV", "value": str(var1) }
    var2 = ppc_master_obj.q_actual_mv*ppc_master_obj.S_nom
    message2 = { "destination": "localPlatform", "value_name": "reactive_power_MV", "value": str(var2) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
    except:
        print('MV quantities Error')

# --- HV quantities -------------------------------------------

def send_HV_quantities(ppc_master_obj):
    var1 = ppc_master_obj.p_actual_hv*ppc_master_obj.S_nom
    message1 = { "destination": "localPlatform", "value_name": "active_power_HV", "value": str(var1) }
    var2 = ppc_master_obj.q_actual_hv*ppc_master_obj.S_nom
    message2 = { "destination": "localPlatform", "value_name": "reactive_power_HV", "value": str(var2) }
    message3 = { "destination": "localPlatform", "value_name": "frequency_HV", "value": str(ppc_master_obj.f_actual) }
    I = math.sqrt(ppc_master_obj.p_actual_hv**2 + ppc_master_obj.q_actual_hv**2)/ppc_master_obj.v_actual
    I = I*ppc_master_obj.S_nom/0.15 # MVA/MV = A
    message4 = { "destination": "localPlatform", "value_name": "current_HV", "value": str(I) }
    V = ppc_master_obj.v_actual*150
    message5 = { "destination": "localPlatform", "value_name": "voltage_HV", "value": str(V) }
    if ppc_master_obj.p_actual_hv == 0: PF = 1
    else: PF = math.cos(math.atan(ppc_master_obj.q_actual_hv/ppc_master_obj.p_actual_hv))
    message6 = { "destination": "localPlatform", "value_name": "PF", "value": str(PF) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
        socket_tx.send_json(message3, zmq.NOBLOCK)
        socket_tx.send_json(message4, zmq.NOBLOCK)
        socket_tx.send_json(message5, zmq.NOBLOCK)
        socket_tx.send_json(message6, zmq.NOBLOCK)
    except:
        print('HV quantities Error')

# --- Running setpoints --------------------------------------

def send_actual_setpoints(ppc_master_obj):
    var1 = ppc_master_obj.p_ex_sp*ppc_master_obj.S_nom
    message1 = { "destination": "localPlatform", "value_name": "actual_P_setpoint", "value": str(var1) }
    var2 = ppc_master_obj.q_ex_sp*ppc_master_obj.S_nom
    message2 = { "destination": "localPlatform", "value_name": "actual_Q_setpoint", "value": str(var2) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
    except:
        print('Actual setpoints Error')


# --- TSO setpoints -----------------------------------------

def send_remote_setpoints(ppc_master_obj):
    var1 = ppc_master_obj.remote_P_sp*ppc_master_obj.S_nom
    message1 = { "destination": "localPlatform", "value_name": "P_setpoint_remote", "value": str(var1) }
    var2 = ppc_master_obj.remote_Q_sp*ppc_master_obj.S_nom
    message2 = { "destination": "localPlatform", "value_name": "Q_setpoint_remote", "value": str(var2) }
    var3 = ppc_master_obj.remote_PF_sp
    message3 = { "destination": "localPlatform", "value_name": "PF_setpoint_remote", "value": str(var3) }
    var4 = ppc_master_obj.remote_V_sp*ppc_master_obj.V_nom
    message4 = { "destination": "localPlatform", "value_name": "V_setpoint_remote", "value": str(var4) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
        socket_tx.send_json(message3, zmq.NOBLOCK)
        socket_tx.send_json(message4, zmq.NOBLOCK)
    except:
        print('Remote setpoints Error')

# --- Max capability base on meteo ---------------------------

def send_max_capability(ppc_master_obj):
    var1 = ppc_master_obj.max_P_cap*ppc_master_obj.S_nom
    message1 = { "destination": "localPlatform", "value_name": "max_active_capability", "value": str(var1) }
    var2 = ppc_master_obj.max_Q_cap*ppc_master_obj.S_nom
    message2 = {"destination": "localPlatform", "value_name": "max_reactive_capability", "value": str(var2)}
    var3 = ppc_master_obj.min_Q_cap*ppc_master_obj.S_nom
    message3 = { "destination": "localPlatform", "value_name": "min_Q_capability", "value": str(var3) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
        socket_tx.send_json(message3, zmq.NOBLOCK)
    except:
        print('Max capability Error')

# --- Modes of operation -------------------------------------

def send_operation_status(ppc_master_obj):
    message1 = { "destination": "localPlatform", "value_name": "P_control_mode", "value": str(ppc_master_obj.p_mode) }
    message2 = { "destination": "localPlatform", "value_name": "Q_control_mode", "value": str(ppc_master_obj.q_mode) }
    message3 = { "destination": "localPlatform", "value_name": "simulation_start_stop", "value": str(ppc_master_obj.simulation_start_stop) }
    message4 = { "destination": "localPlatform", "value_name": "operational_state", "value": str(ppc_master_obj.operational_state) }
    message5 = { "destination": "localPlatform", "value_name": "Auto_Start_state", "value": str(ppc_master_obj.auto_start_state) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
        socket_tx.send_json(message3, zmq.NOBLOCK)
        socket_tx.send_json(message4, zmq.NOBLOCK)
        socket_tx.send_json(message5, zmq.NOBLOCK)
    except:
        print('Operation status Error')

# --- Meteo --------------------------------------------------

def send_meteo(ppc_master_obj):
    message1 = { "destination": "localPlatform", "value_name": "temperature", "value": str(round(ppc_master_obj.temp, 2)) }
    message2 = { "destination": "localPlatform", "value_name": "total_irradiance", "value": str(round(ppc_master_obj.irradiance, 2)) }
    message3 = { "destination": "localPlatform", "value_name": "sunrise", "value": str(ppc_master_obj.sunrise) }
    message4 = { "destination": "localPlatform", "value_name": "sunset", "value": str(ppc_master_obj.sunset) }
    try:
        socket_tx.send_json(message1, zmq.NOBLOCK)
        socket_tx.send_json(message2, zmq.NOBLOCK)
        socket_tx.send_json(message3, zmq.NOBLOCK)
        socket_tx.send_json(message4, zmq.NOBLOCK)
    except:
        print('Meteo Error')

def scada_tx(ppc_master_obj):
    send_MV_quantities(ppc_master_obj)
    send_HV_quantities(ppc_master_obj)
    send_actual_setpoints(ppc_master_obj)
    send_remote_setpoints(ppc_master_obj)
    send_max_capability(ppc_master_obj)
    send_operation_status(ppc_master_obj)
    send_meteo(ppc_master_obj)