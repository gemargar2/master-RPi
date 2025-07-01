import threading
from scada_rx import *
from scada_tx import *
from tso_rx import *
from hvmeter_rx import *
from controller_core import *
from class_def import *
from limit import *

def main():
    # Load last setpoint values before shutting down
    with open('setpoints.json', 'r') as openfile:
        memory = json.load(openfile)
    
    with open('configfile.json', 'r') as openfile:
        config = json.load(openfile)

    # Create objects
    ppc_master_obj = PPC_master_class(memory, config)
    window_obj = Window_class()

    # Start parallel processes
    # Scans Tsotakis IP for signals comming from SCADA
#     scada_receive = threading.Thread(target = scada_rx, args=(ppc_master_obj, window_obj))
#     scada_receive.start()
#     scada_send = threading.Thread(target l= scada_tx, args=(ppc_master_obj,))
#     scada_send.start()
    # Scans local IP for signals comming from TSO
    tsoApp = threading.Thread(target = tso_rx, args=(ppc_master_obj, window_obj))
    tsoApp.start()
    # Scans local IP for signals comming from HV meter
    hvmeterApp = threading.Thread(target = hvmeter_rx, args=(ppc_master_obj,))
    hvmeterApp.start()

    # Initialize Q-U with limit curve
    ppc_master_obj.V_Limit_VDE_init(q_ref=0.0)
    ppc_master_obj.QP_init()
    window_obj.plot_PF_curve(ppc_master_obj)
    window_obj.plot_QU_curve(ppc_master_obj)
    window_obj.plot_QU_limit_curve(ppc_master_obj)
    window_obj.plot_QP_curve(ppc_master_obj)

    # Start looping controller core
    i = 0
    while True:
        controllerCore(i, window_obj, ppc_master_obj)
        i += 1

if __name__ == "__main__":
    main()
    # while not shutdown:
    #     q = float(input("Q setpoint = "))
    #     v = float(input("V actual = "))
    #     UQ_limit(q, v)
    #     q = float(input("Q setpoint = "))
    #     p = float(input("P actual = "))
    #     PQ_limit(q, p)


