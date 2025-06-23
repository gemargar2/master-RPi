from header import *

printMessages = False

def send_P_in_sp(p_in_sp):
    try:
        message = {"destination": "device", "id": "0", "value_name": "P_setpoint", "value": str(p_in_sp)}
        device_socket_tx.send_json(message, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('P internal setpoint error')

def send_Q_in_sp(q_in_sp):
    try:
        message = {"destination": "device", "id": "0", "value_name": "Q_setpoint", "value": str(q_in_sp)}
        device_socket_tx.send_json(message, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('Q internal setpoint error')

def send_P_ex_sp(p_ex_sp):
    try:
        message = {"destination": "device", "id": "0", "value_name": "P_ex_sp", "value": str(p_ex_sp)}
        device_socket_tx.send_json(message, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('P external setpoint error')

def send_Q_ex_sp(q_ex_sp):
    try:
        message = {"destination": "device", "id": "0", "value_name": "Q_ex_sp", "value": str(q_ex_sp)}
        device_socket_tx.send_json(message, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('Q external setpoint error')

def device_tx(p_in_sp, q_in_sp, p_ex_sp, q_ex_sp):
    # PV production is measured on MV
    send_P_in_sp(p_in_sp)
    send_Q_in_sp(q_in_sp)
    send_P_ex_sp(p_ex_sp)
    send_Q_ex_sp(q_ex_sp)