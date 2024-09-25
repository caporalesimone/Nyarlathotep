""" This module provides network information about the host machine. """

from typing import List, Dict, Any
from collections import defaultdict
import socket
import psutil

class NetworkInfo:
    """ Network Info Class """

    @staticmethod
    def get_host_name() -> str:
        """ Get host name """

        try:
            return socket.gethostname()
        except Exception as e:
            raise RuntimeError(f"Error during host name query: {e}") from e

    @staticmethod
    def get_network_name() -> str:
        """ Get network name """

        try:
            return socket.getfqdn()
        except Exception as e:
            raise RuntimeError(f"Error during network name query: {e}") from e

    @staticmethod
    def get_network_interfaces(family: int = socket.AF_INET) -> List[Dict[str, Any]]:
        """ Get network interfaces """

        interfaces = defaultdict(lambda: {"mac_address": None, "ip_addresses": []})

        # Get active network interfaces
        try:
            active_interfaces = {name for name, stats in psutil.net_if_stats().items()
                                 if stats.isup}
        except Exception as e:
            raise RuntimeError(f"Error during network interfaces query: {e}") from e

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
            raise RuntimeError(f"Error during network interfaces query: {e}") from e

        # Format the result into a list of dictionaries
        result = [
            {
             "interface": interface, 
             "mac": info["mac_address"], 
             "ip_addresses": info["ip_addresses"]
             }
            for interface, info in interfaces.items()
        ]

        return result
