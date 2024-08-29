from network_info import NetworkInfo
from os_info import OSInfo
from hardware_info import HardwareInfo
from user_info import UserInfo

class DataCollector:
    def __init__(self) -> None:
        self.hostname = NetworkInfo.get_host_name()
        self.network_name = NetworkInfo.get_network_name()
        self.net_interfaces = NetworkInfo.get_network_interfaces()
        self.os = OSInfo()
        self.hardware = HardwareInfo()
        self.users = UserInfo.get_logged_users()