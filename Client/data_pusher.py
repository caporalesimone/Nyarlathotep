import requests
import json
import time
from data_collector import DataCollector
from versions import JSON_VERSION

class DataPusher:
    def __init__(self, client_sw_version, client_name, remote_server_url) -> None:
        self.client_sw_version = client_sw_version
        self.json_version = JSON_VERSION
        self.client_name = client_name
        self.remote_server_url = remote_server_url

    def push_new_data(self):
        data = DataCollector()
        self.last_json_data = {
            "client_name": self.client_name,
            "client_sw_version": self.client_sw_version,
            "local_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "json_version": self.json_version,
            "hostname": data.hostname,
            "network_name": data.network_name,
            "net_interfaces": data.net_interfaces,
            "os": data.os,
            "hardware": data.hardware,
            "users": data.users,
        }

        self.last_json = json.dumps(self.last_json_data, default=lambda o: o.__dict__, indent=2)

        try:
            response = requests.post(self.remote_server_url, data=self.last_json, headers={"Content-Type": "application/json; charset=utf-8"})
            if response.status_code == 200:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"{timestamp} - Data successfully sent")
            else:
                print(f"Error sending data: HTTP ERROR {response.status_code}")
        except Exception as e:
            print(f"Error sending data to server: {e}")
