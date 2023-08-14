import socket

def get_reflection_ratio(ip, port=123):
    # 构造一个NTP请求，例如monlist查询
    request = b'\x17\x00\x03\x2a' + b'\x00' * 4

    try:
        # 创建一个UDP套接字并连接到NTP服务器
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.sendto(request, (ip, port))
            response, _ = s.recvfrom(2048)

            # 计算反射倍数
            return len(response) / len(request)
    except (socket.timeout, OSError):
        return 0

def find_top_reflectors(filename="server.txt", top_n=50, output_file="top.txt"):
    servers_reflection_ratios = []

    with open(filename, "r") as file:
        for line in file:
            ip = line.strip()
            ratio = get_reflection_ratio(ip)
            servers_reflection_ratios.append((ip, ratio))
            print(f"服务器 {ip} 的反射倍数: {ratio}")

    # 按反射倍数降序排序
    servers_reflection_ratios.sort(key=lambda x: x[1], reverse=True)

    # 获取反射倍数最大的N个服务器
    top_reflectors = servers_reflection_ratios[:top_n]

    print("\n反射倍数最大的服务器:")
    with open(output_file, "w") as file:
        for ip, ratio in top_reflectors:
            print(f"IP: {ip}, 反射倍数: {ratio}")
            file.write(f"{ip}\n")

    print(f"\n保存了反射倍数最大的 {top_n} 个服务器到 {output_file}")


if __name__ == "__main__":
    find_top_reflectors()