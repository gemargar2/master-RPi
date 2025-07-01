import zmq
from remote_callbacks import *
from local_callbacks import *
import time

def hvmeter_rx(ppc_master_obj):
    
    while True:
        # Wait for command
        message = ppc_master_obj.socket_rx.recv_json()
        # print(message)
        if message['origin'] == 'HV_Meter':
            # print(message)
            if message['value_name'] == 'VAC_ph': ppc_master_obj.v_actual = float(message["value"])
            elif message['value_name'] == 'f': ppc_master_obj.f_actual = float(message["value"])
            elif message['value_name'] == 'Pa': ppc_master_obj.p_actual_hv = float(message["value"])
            elif message['value_name'] == 'Qa': ppc_master_obj.q_actual_hv = float(message["value"])
        
        elif message['origin'] == 'Slave':
            # print(message)
            if message['id'] == "13":
                if message['value_name'] == 'temperature': ppc_master_obj.temp = float(message["value"])
                elif message['value_name'] == 'Direct Irradiance': ppc_master_obj.irradiance = float(message["value"])
                
                