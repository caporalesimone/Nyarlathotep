import json
import requests
import psutil
import socket
import platform
import time
import os
from configparser import ConfigParser
from typing import List

CONFIG_FILE = 'config.ini'

# Default values
DEFAULT_CUSTOM_NAME = "WORKSTATION"
DEFAULT_UPDATE_INTERVAL = 30  # in seconds
DEFAULT_REMOTE_SERVER_URL = "http://localhost:8080/client_update"

def load_config():
    config = ConfigParser()

    if not os.path.exists(CONFIG_FILE):
        config['SETTINGS'] = {
            'CUSTOM_NAME': DEFAULT_CUSTOM_NAME,
            'UPDATE_INTERVAL': str(DEFAULT_UPDATE_INTERVAL),
            'REMOTE_SERVER_URL': DEFAULT_REMOTE_SERVER_URL
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        print(f"Config file created with default values at {CONFIG_FILE}")

    config.read(CONFIG_FILE)

    if not config.has_option('SETTINGS', 'CUSTOM_NAME'):
        config.set('SETTINGS', 'CUSTOM_NAME', DEFAULT_CUSTOM_NAME)
        updated = True
    else:
        updated = False

    if not config.has_option('SETTINGS', 'UPDATE_INTERVAL'):
        config.set('SETTINGS', 'UPDATE_INTERVAL', str(DEFAULT_UPDATE_INTERVAL))
        updated = True

    if not config.has_option('SETTINGS', 'REMOTE_SERVER_URL'):
        config.set('SETTINGS', 'REMOTE_SERVER_URL', DEFAULT_REMOTE_SERVER_URL)
        updated = True

    if updated:
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        print(f"Config file updated with missing default values at {CONFIG_FILE}")

    custom_name = config.get('SETTINGS', 'CUSTOM_NAME')
    update_interval = config.getint('SETTINGS', 'UPDATE_INTERVAL')
    remote_server_url = config.get('SETTINGS', 'REMOTE_SERVER_URL')

    print(f"Custom Name: {custom_name}")
    print(f"Update Interval: {update_interval}")
    print(f"Remote Server URL: {remote_server_url}")

    return custom_name, update_interval, remote_server_url

class User:
    def __init__(self, username, fullname, logged, login_time):
        self.username = username
        self.fullname = fullname
        self.logged = logged
        self.login_time = login_time

class ClientUpdate:
    def __init__(self, custom_name, hostname, ip_addresses, os, total_memory, used_memory, cpu_usage, disk_size, disk_used, users: List[User]):
        self.customName = custom_name
        self.hostname = hostname
        self.ipAddresses = ip_addresses
        self.os = os
        self.total_memory = total_memory
        self.used_memory = used_memory
        self.cpu_usage = cpu_usage
        self.disk_size = disk_size
        self.disk_used = disk_used
        self.users = users

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

def get_ip_addresses():
    host_name = socket.gethostname()
    return socket.gethostbyname_ex(host_name)[2]

def get_memory_info():
    memory = psutil.virtual_memory()
    total_memory = memory.total // (1024 * 1024)  # in MB
    used_memory = memory.used // (1024 * 1024)    # in MB
    return total_memory, used_memory

def get_disk_info():
    disk = psutil.disk_usage('/')
    disk_size = disk.total // (1024 * 1024 * 1024)  # in GB
    disk_used = disk.used // (1024 * 1024 * 1024)   # in GB
    return disk_size, disk_used

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_os_info():
    return platform.system() + " " + platform.release() + " "

def get_logged_in_users():
    users = []
    for user in psutil.users():
        username = user.name
        fullname = username  # Using username as fullname for simplicity
        logged = True # Always True for now
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.started))
        users.append(User(username, fullname, logged, login_time))
    return users

CUSTOM_NAME, UPDATE_INTERVAL, REMOTE_SERVER_URL = load_config()

while True:
    hostname = socket.gethostname()
    ip_addresses = get_ip_addresses()
    os_name = get_os_info()
    total_memory, used_memory = get_memory_info()
    cpu_usage = get_cpu_usage()
    disk_size, disk_used = get_disk_info()
    users = get_logged_in_users()

    client_update = ClientUpdate(
        custom_name=CUSTOM_NAME,
        hostname=hostname,
        ip_addresses=ip_addresses,
        os=os_name,
        total_memory=total_memory,
        used_memory=used_memory,
        cpu_usage=cpu_usage,
        disk_size=disk_size,
        disk_used=disk_used,
        users=users
    )

    json_data = client_update.to_json()

    response = requests.post(REMOTE_SERVER_URL, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f"{timestamp} - Data successfully sent")
    else:
        print(f"Error sending data: HTTP ERROR {response.status_code}")

    time.sleep(UPDATE_INTERVAL)
