"""	DataPusher class is responsible for sending the data to the remote server. """

import json
import time
import requests
from data_collector import DataCollector
from versions import JSON_VERSION

class DataPusher:
    """DataPusher class is responsible for sending the data to the remote server."""

    def __init__(self, client_sw_version, client_name, remote_server_url, project_name) -> None:
        self.client_sw_version = client_sw_version
        self.json_version = JSON_VERSION
        self.client_name = client_name
        self.remote_server_url = remote_server_url
        self.project_name = project_name
        self.collected_data = {}
        self.last_json = None

    def push_new_data(self) -> None:
        """Push new data to the remote server."""	

        data = DataCollector()
        self.collected_data = {
            "client_name": self.client_name,
            "client_sw_version": self.client_sw_version,
            "local_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "json_version": self.json_version,
            "project_name": self.project_name,
            "hostname": data.hostname,
            "network_name": data.network_name,
            "net_interfaces": data.net_interfaces,
            "os": data.os,
            "hardware": data.hardware,
            "users": data.users,
        }

        self.last_json = json.dumps(self.collected_data, default=lambda o: o.__dict__, indent=2)

        try:
            response = requests.post(self.remote_server_url,
                                     data=self.last_json,
                                     headers={"Content-Type": "application/json; charset=utf-8"},
                                     timeout=10)  # Add a timeout value (e.g., 10 seconds)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"{timestamp} - Data successfully sent")
            else:
                print(f"Error sending data: HTTP ERROR {response.status_code}")
                print(f"Response body: {response.text}")
                print(f"JSON sent: {self.last_json}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to server: {e}")
