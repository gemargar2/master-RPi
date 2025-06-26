
printMessages = False

v_ref = 1.0 # Voltage setpoint is always 1.0 p.u

# Q mode = 2
def V_control(ppc_master_obj):
    q_ref = ppc_master_obj.q_ex_sp
    v_actual = ppc_master_obj.v_actual
    
    if ppc_master_obj.local_remote == 0: v_sp = ppc_master_obj.local_V_sp # setpoint voltage
    else: v_sp = ppc_master_obj.remote_V_sp # setpoint voltage

    slope = ppc_master_obj.slope_sp # Droop adjustable between 2-12%, default value 5%
    db = ppc_master_obj.V_deadband_sp # voltage deadband
    m = 1/slope # gradient 7<m<24

    if (v_actual < v_sp - db):
        if printMessages:
            print(f'{v_actual} < {v_sp - db}')
            print("Under voltage")
        delta_V = (v_sp - db) - v_actual
        delta_Q = delta_V * m
        q_in_sp = q_ref + delta_Q
    elif (v_actual > v_sp + db):
        if printMessages:
            print(f'{v_actual} > {v_sp + db}')
            print("Over voltage")
        delta_V = v_actual - (v_sp + db)
        delta_Q = delta_V * m
        q_in_sp = q_ref - delta_Q
    else:
        q_in_sp = q_ref

    return q_in_sp

# Q mode = 3 (PF Control)
# Q mode = 4 (Q Open Loop)

# Q mode = 5
def QU_VDE(ppc_master_obj):
    q_ref = ppc_master_obj.q_ex_sp
    v_actual = ppc_master_obj.v_actual
    slope = 0.05 # Droop adjustable between 2-12%, default value 5%
    v_sp = 1.0 # setpoint voltage
    db = 0.02 # voltage deadband
    m = 1/slope # gradient 7<m<24

    if (v_actual < v_sp - db):
        if printMessages:
            print(f'{v_actual} < {v_sp - db}')
            print("Under voltage")
        delta_V = (v_sp - db) - v_actual
        delta_Q = delta_V * m
        q_in_sp = q_ref + delta_Q
    elif (v_actual > v_sp + db):
        if printMessages:
            print(f'{v_actual} > {v_sp + db}')
            print("Over voltage")
        delta_V = v_actual - (v_sp + db)
        delta_Q = delta_V * m
        q_in_sp = q_ref - delta_Q
    else:
        q_in_sp = q_ref

    return q_in_sp

# Q mode = 6
def V_Limit_VDE(ppc_master_obj):
    q_ref = ppc_master_obj.q_ex_sp
    v_actual = ppc_master_obj.v_actual
    if (v_actual < ppc_master_obj.dba):
        if printMessages:
            print(f'{v_actual} < {ppc_master_obj.dba}')
            print("Under voltage")
        delta_V = ppc_master_obj.dba - v_actual
        delta_Q = delta_V * abs(ppc_master_obj.ma)
        q_in_sp = q_ref + delta_Q
    elif (v_actual > ppc_master_obj.dbb):
        if printMessages:
            print(f'{v_actual} > {ppc_master_obj.dbb}')
            print("Over voltage")
        delta_V = v_actual - ppc_master_obj.dbb
        delta_Q = delta_V * abs(ppc_master_obj.mb)
        q_in_sp = q_ref - delta_Q
    else:
        q_in_sp = q_ref

    return q_in_sp

