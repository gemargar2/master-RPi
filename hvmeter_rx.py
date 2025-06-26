import zmq
from remote_callbacks import *
from local_callbacks import *

def hvmeter_rx(ppc_master_obj):
    # Real
    context_rx = zmq.Context()
    socket_rx = context_rx.socket(zmq.PULL)
    socket_rx.connect("tcp://160.40.48.99:2002") # Receive directly from emulator

    while True:
        # Wait for command
        message = socket_rx.recv_json()

        if message['origin'] == 'HVmeter':
            # print(message)
            if message['value_name'] == 'VAC_ph': ppc_master_obj.v_actual = float(message["value"])
            elif message['value_name'] == 'f': ppc_master_obj.f_actual = float(message["value"])
            elif message['value_name'] == 'Pa': ppc_master_obj.p_actual_hv = float(message["value"])
            elif message['value_name'] == 'Qa': ppc_master_obj.q_actual_hv = float(message["value"])
        
        elif message['origin'] == 'MVmeter_main':
            # print(message)
            if message['value_name'] == 'Pa': ppc_master_obj.p_actual_mv = float(message["value"])
            elif message['value_name'] == 'Qa': ppc_master_obj.q_actual_mv = float(message["value"])
        
        elif message['origin'] == 'slave':
            if message['id'] == "13":
                if message['value_name'] == 'temperature': ppc_master_obj.temp = float(message["value"])
                elif message['value_name'] == 'Direct Irradiance': ppc_master_obj.irradiance = float(message["value"])
                
                