import zmq

printMessages = False

def send_internal_setpoints(ppc_master_obj, p_in_sp, q_in_sp):
    try:
        message1 = {"destination": "Slave", "id": "0", "value_name": "P_SP_master", "value": str(p_in_sp)}
        message2 = {"destination": "Slave", "id": "0", "value_name": "Q_SP_master", "value": str(q_in_sp)}
        ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
        ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('Slave internal setpoints Error')

def send_external_setpoints(ppc_master_obj, p_ex_sp, q_ex_sp):
    try:
        message = {"destination": "device", "id": "0", "value_name": "P_ex_sp", "value": str(p_ex_sp)}
        message = {"destination": "device", "id": "0", "value_name": "Q_ex_sp", "value": str(q_ex_sp)}
        ppc_master_obj.socket_tx.send_json(message1, zmq.NOBLOCK)
        ppc_master_obj.socket_tx.send_json(message2, zmq.NOBLOCK)
        if printMessages: print("Success")
    except:
        if printMessages: print('Slave external setpoint error')

def slave_tx(ppc_master_obj, p_in_sp, q_in_sp, p_ex_sp, q_ex_sp):
    send_internal_setpoints(ppc_master_obj, p_in_sp, q_in_sp)