import subprocess
import threading
import socketio
import config
import psutil
import signal
import fcntl
import time
import pty
import os
import re

sio = socketio.Client()
last_request = time.time()
def start_bash_session():
    master_fd, slave_fd = pty.openpty()
    fcntl.fcntl(master_fd, fcntl.F_SETFL, fcntl.fcntl(master_fd, fcntl.F_GETFL) | os.O_NONBLOCK)
    bash_session = subprocess.Popen(
        ['/bin/bash'],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        text=True,
        bufsize=1,
        universal_newlines=True,
        preexec_fn=os.setsid
    )
    return master_fd, bash_session
master_fd, bash_session = start_bash_session()
ansi_pattern = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])|(?:\x1B\[.*?[a-zA-Z])')

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('request_network_state')
def on_network_state_request(data):
    update_last_request()
    request_type = data.get('request_type')
    
    if request_type == 'ifconfig':
        network_data = os.popen("ifconfig").read()
    elif request_type == 'netstat':
        network_data = os.popen("netstat -tulpn").read()
    elif request_type == 'ping':
        server_ip = '1.1.1.1'
        network_data = os.popen(f"ping -c 4 {server_ip}").read()
    
    sio.emit('network_state', {'state': network_data})

@sio.on('request_wifi_clients')
def on_request_wifi_clients():
    update_last_request()
    results = os.popen("iwlist wlan0 scan | awk -F: '/ESSID/{gsub(/\"/, \"\", $2); ssid=$2} /Signal level/{split($0, a, \"=\"); print ssid, a[3]}' | sort -k2 -n -r").read()
    sio.emit('pi_data_result', {'wifi_clients': results})

@sio.on('request_reboot')
def on_request_reboot():
    sio.emit('pi_data_result', {'power_request': "Reboot request sent."})
    os.popen("reboot")

@sio.on('request_shutdown')
def on_request_shutdown():
    sio.emit('pi_data_result', {'power_request': "Shutdown request sent."})
    os.popen("shutdown now")

@sio.on('request_wifi')
def on_request_wifi():
    update_last_request()
    output = os.popen('ip link show wlan0').read()
    if "state UP" in output:
        os.popen('ip link set wlan0 down')
    else:
        os.popen('ip link set wlan0 up')

@sio.on('refresh')
def on_refresh():
    update_last_request()
    send_periodic_data()
    
@sio.on('request_connect_wifi')
def connect_to_wifi(data):
    update_last_request()
    ssid = data.get('ssid')
    password =  data.get('password')
    wpa_config = f"""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}
    """
    
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
        file.write(wpa_config)
    
    os.system('killall wpa_supplicant')
    os.system(f'rm /var/run/wpa_supplicant/wlan0')
    os.system(f'wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf')
    time.sleep(2)
    os.popen('dhclient wlan0').read()
    print(f"Connected to {ssid}")

@sio.on('request_ssh_interrupt')
def request_ssh_interrupt():
    update_last_request()
    global master_fd, bash_session
    os.killpg(os.getpgid(bash_session.pid), signal.SIGINT)
    bash_session.kill()
    bash_session.wait()
    master_fd, bash_session = start_bash_session()
@sio.on('request_send_command')
def request_send_command(data):
    update_last_request()
    command = data.get('command')
    os.write(master_fd, (command + "\n").encode('utf-8'))

def monitor_output():
    buffer = ""
    while True:
        time.sleep(0.5)
        try:
            output = os.read(master_fd, 1024).decode()
            if output:
                buffer += output
                print(output, end='', flush=True)
                sio.emit('cmd_result', {'result': ansi_pattern.sub('', output)})
        except:
            pass

def get_disk_usage():
    disk_data = os.popen("df -h /").readlines()[1].split()
    return f"Filesystem: {disk_data[0]}, Size: {disk_data[1]}, Used: {disk_data[2]}, Available: {disk_data[3]}, Usage: {disk_data[4]}"

def get_core_status():
    temp = os.popen("vcgencmd measure_temp").read().strip().replace("temp=", "Temperature: ")
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    uptime = os.popen("uptime -p").read().strip().replace("up ", "Uptime: ")
    
    return f"{temp}, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%, {uptime}"

def get_wifi_status():
    output = os.popen('ip link show wlan0').read()
    if "state UP" in output:
        ssid = os.popen('iwgetid -r').read()
        return (f"Wi-Fi is ON | Connected to {ssid}") if ssid != "" else (f"Wi-Fi is ON")
    else:
        return "Wi-Fi is OFF"

def update_last_request():
    global last_request
    last_request = time.time()

def send_periodic_data():
    try:
        data = {
            'disk_usage': get_disk_usage(),
            'core_status': get_core_status(),
            'wifi_state': get_wifi_status()
        }
        sio.emit('pi_data', data)
    except: pass

if __name__ == '__main__':
    sio.connect(config.server_url)
    monitor_thread = threading.Thread(target=monitor_output, daemon=True)
    monitor_thread.start()
    while True:
        if last_request > time.time() - 60:
            send_periodic_data()
        time.sleep(5)
