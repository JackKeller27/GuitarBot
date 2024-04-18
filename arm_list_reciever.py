import socket

import time

import RobotControllerAmit
from ast import literal_eval
from parsing.ArmListParser import ArmListParser
import RobotControllerAmit

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip = "127.0.0.1" #UDP_IP
udp_port = 40012 #UDP_PORT
left_arm_header = "l_arm_guitar"
right_arm_header = "r_arm_guitar"
measure_time_header = "measure_time_guitar"

time.sleep(1)
socket.bind((udp_ip, udp_port))

left_arm = None
right_arm = None
measure_time = None

# loop to recieve messages and send to robot controller
while True:
    recieved_msg = socket.recv(1024) # 1024 byte buffer size
    recieved_msg = recieved_msg.decode("utf-8")

    # parse message
    split = recieved_msg.split('#')
    msg_header = split[0]
    msg_body = split[1]
    print("message header: ", msg_header)

    if msg_header == left_arm_header:
        left_arm = literal_eval(msg_body)
    elif msg_header == right_arm_header:
        right_arm = literal_eval(msg_body)
    elif msg_header == measure_time_header:
        measure_time = float(msg_body)
    else:
        print("Message header not recognized: ", msg_header)

    print("message body: ", msg_body)

    print(left_arm)
    print(right_arm)
    print(measure_time)

    if left_arm is not None and right_arm is not None and measure_time is not None:
        # parse arm lists
        left_arm_info, first_c, m_timings = ArmListParser.parseleft_M(left_arm, measure_time)
        right_arm_info, initial_strum, strum_onsets = ArmListParser.parseright_M(right_arm, measure_time)

        print("right_arm_info", right_arm_info)
        print("left_arm_info", left_arm_info)
        print("first_c: ", first_c)
        print("m_timings: ", m_timings)
        print("initial_strum: ", initial_strum)
        print("strum_onsets: ", strum_onsets)

        # send song data to robot controller
        RobotControllerAmit.main(right_arm_info, left_arm_info, first_c, measure_time, m_timings, strum_onsets)