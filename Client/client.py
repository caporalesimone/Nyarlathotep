import json
import requests
import psutil
import socket
import platform
import time
from typing import List

CUSTOM_NAME = "AG2"
UPDATE_INTERVAL = 30  # Update interval in seconds

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
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

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
        logged = True
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.started))
        users.append(User(username, fullname, logged, login_time))
    return users

url = "http://localhost:8080/client_update"

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

    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Data successfully sent!")
    else:
        print(f"Error sending data: {response.status_code}")

    time.sleep(UPDATE_INTERVAL)
