import socket
import psutil
from typing import List, Dict, Any
from collections import defaultdict

class NetworkInfo:
    @staticmethod
    def get_network_interfaces(family: int = socket.AF_INET) -> List[Dict[str, Any]]:
        interfaces = defaultdict(lambda: {"mac_address": None, "ip_addresses": []})

        # Get active network interfaces
        try:
            active_interfaces = {name for name, stats in psutil.net_if_stats().items() if stats.isup}
        except Exception as e:
            raise RuntimeError(f"Error during network interfaces query: {e}")

        # Get MAC and IP addresses for each active interface
        try:
            for interface, snics in psutil.net_if_addrs().items():
                if interface in active_interfaces:
                    for snic in snics:
                        if snic.family == psutil.AF_LINK:  # Type MAC Address
                            interfaces[interface]["mac_address"] = snic.address
                        elif snic.family == family:  # Type IP Address
                            if snic.address != "127.0.0.1":  # Ignore loopback address
                                interfaces[interface]["ip_addresses"].append(snic.address)
        except Exception as e:
            raise RuntimeError(f"Error during network interfaces query: {e}")

        # Format the result into a list of dictionaries
        result = [
            {"interface": interface, "mac": info["mac_address"], "ip_addresses": info["ip_addresses"]}
            for interface, info in interfaces.items()
        ]

        return result