import requests
import json
import time
from data_collector import DataCollector

class DataPusher:
    def __init__(self, client_name, remote_server_url) -> None:
        self.client_name = client_name
        self.remote_server_url = remote_server_url

    def push_new_data(self):
        data = DataCollector()
        self.last_json_data = {
            "client_name": self.client_name,
            "local_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "hostname": data.hostname,
            "network_name": data.network_name,
            "net_interfaces": data.net_interfaces,
            "os": data.os,
            "hardware": data.hardware,
            "users": data.users,
        }

        self.last_json = json.dumps(self.last_json_data, default=lambda o: o.__dict__, indent=2)

        response = requests.post(self.remote_server_url, data=self.last_json, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"{timestamp} - Data successfully sent")
        else:
            print(f"Error sending data: HTTP ERROR {response.status_code}")
