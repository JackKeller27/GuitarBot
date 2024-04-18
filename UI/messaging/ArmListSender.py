import socket
from socket import INADDR_ANY


class ArmListSender:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_ip = "127.0.0.1"  #UDP_IP
        self.udp_port = 40012  #UDP_PORT
        self.left_arm_header = "l_arm_guitar#"
        self.right_arm_header = "r_arm_guitar#"
        self.measure_time_header = "measure_time_guitar#"

    def send_arm_lists_to_reciever(self, left_arm, right_arm, measure_time):
        # send left arm data
        msg = self.left_arm_header + str(left_arm)
        self.socket.sendto(msg.encode("utf-8"), (self.udp_ip, self.udp_port))

        # send right arm data
        msg = self.right_arm_header + str(right_arm)
        self.socket.sendto(msg.encode("utf-8"), (self.udp_ip, self.udp_port))

        # send measure time
        msg = self.measure_time_header + str(measure_time)
        self.socket.sendto(msg.encode("utf-8"), (self.udp_ip, self.udp_port))
