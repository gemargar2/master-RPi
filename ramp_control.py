import math

# --- PID controllers --------------------------------

def p_pid_controller(setpoint, pv, kp, ki, kd, previous_error, integral, dt):
    error = setpoint - pv
    integral += error * dt
    derivative = 0 # (error - previous_error) / dt
    control = kp * error + ki * integral + kd * derivative

    return control, error, integral

def q_pid_controller(setpoint, pv, kp, ki, kd, previous_error, integral, dt):
    error = setpoint - pv
    integral += error * dt
    derivative = 0 # (error - previous_error) / dt
    control = kp * error + ki * integral + kd * derivative

    return control, error, integral

# --- Gradient control -------------------------------

prev_p_sp = 0
prev_q_sp = 0

def ramp_rate(ppc_master_obj):
    global prev_p_sp , prev_q_sp

    ppc_master_obj.Q_grad = ppc_master_obj.P_grad

    if ppc_master_obj.p_mode == 3: # MPPT
        grad = ppc_master_obj.MPPT_grad
    else: # P Control or P Open Loop
        grad = ppc_master_obj.P_grad

    if (ppc_master_obj.p_ex_sp - prev_p_sp > grad):
        prev_p_sp += grad
    elif (prev_p_sp - ppc_master_obj.p_ex_sp > grad):
        prev_p_sp -= grad
    else:
        prev_p_sp = ppc_master_obj.p_ex_sp

    if (ppc_master_obj.q_ex_sp - prev_q_sp > ppc_master_obj.Q_grad):
        prev_q_sp += ppc_master_obj.Q_grad
    elif (prev_q_sp - ppc_master_obj.q_ex_sp> ppc_master_obj.Q_grad):
        prev_q_sp -= ppc_master_obj.Q_grad
    else:
        prev_q_sp = ppc_master_obj.q_ex_sp

    return prev_p_sp, prev_q_sp

# --- Active power ---------------------------------

# PID aux variables
p_prev_error = 0
q_prev_error = 0
p_integral = 0
q_integral = 0

# P mode = 0
def P_control(p_grad_sp, prev_p_in_sp, ppc_master_obj):
    global p_integral, p_prev_error
    # Parameters
    kp = ppc_master_obj.p_kp   # Proportional gain
    ki = ppc_master_obj.p_ki   # Integral gain
    kd = ppc_master_obj.p_kd   # Derivative gain
    dt = ppc_master_obj.p_dt   # 100 ms
    # Power control model
    p_control, p_error, p_integral = p_pid_controller(p_grad_sp, ppc_master_obj.p_actual_hv, kp, ki, kd, p_prev_error, p_integral, dt)
    p_in_sp = prev_p_in_sp + p_control * dt
    p_prev_error = p_error
    
    return p_in_sp

# --- Rective power ---------------------------------

# Q mode = 0
def Q_control(q_grad_sp, prev_q_in_sp, ppc_master_obj):
    global q_integral, q_prev_error, q_in_sp
    # Parameters
    kp = ppc_master_obj.q_kp   # Proportional gain
    ki = ppc_master_obj.q_ki   # Integral gain
    kd = ppc_master_obj.q_kd   # Derivative gain
    dt = ppc_master_obj.q_dt   # 100 ms
    # Power control model
    q_control, q_error, q_integral = q_pid_controller(q_grad_sp, ppc_master_obj.q_actual_hv, kp, ki, kd, q_prev_error, q_integral, dt)
    q_in_sp = prev_q_in_sp + q_control * dt
    q_prev_error = q_error

    return q_in_sp

# Q mode = 1
def QP_control(ppc_master_obj):
    index = 0
    for i in range(ppc_master_obj.numOfPoints-1):
        if (ppc_master_obj.p_actual_hv < ppc_master_obj.P_points[i+1]) and (ppc_master_obj.p_actual_hv > ppc_master_obj.P_points[i]):
            index = i
            break
    # print(index)
    q_in_sp = (ppc_master_obj.p_actual_hv - ppc_master_obj.P_points[index])*ppc_master_obj.m[i] + ppc_master_obj.Q_points[i]
    return q_in_sp

# Q mode = 3
def PF_control(ppc_master_obj):
    q_in_sp = ppc_master_obj.p_actual_hv * math.tan(math.acos(ppc_master_obj.pf_ex_sp))
    return q_in_sp