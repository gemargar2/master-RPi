import matplotlib.pyplot as plt
import time
import zmq
import threading
import math

f_actual = 50
v_actual = 1
p_actual_hv = 0
q_actual_hv = 0
p_in_sp = 0
q_in_sp = 0
p_ex_sp = 0
p_grad_sp = 0
q_ex_sp = 0

dt = 0.1 # 100ms

# Establish connection to send data back to SCADA
context_tx = zmq.Context()
socket_tx = context_tx.socket(zmq.PUSH)
socket_tx.bind("tcp://*:13001")

# Establish connection to forward data to device
device_context_tx = zmq.Context()
device_socket_tx = device_context_tx.socket(zmq.PUSH)
device_socket_tx.bind("tcp://*:13003")

# Initial values
f_ref = 50.0 # Frequency setpoint is always 50.0 Hz
v_ref = 1.0 # Voltage setpoint is always 1.0 p.u

# PID aux variables
f_prev_error = 0
v_prev_error = 0
p_prev_error = 0
q_prev_error = 0
f_integral = 0
v_integral = 0
p_integral = 0
q_integral = 0

# Internal setpoint
f_in_sp = 0
v_in_sp = 0
# p_in_sp = 0
# q_in_sp = 0
p_nsp = 0

v_counter = 0
f_counter = 0