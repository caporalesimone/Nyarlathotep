""" The hardware_info module provides the hardware information of the machine. """	
from typing import Tuple
import platform
import subprocess
import wmi
import psutil

class HardwareInfo:
    """ The HardwareInfo class provides the hardware information. """
    def __init__(self) -> None:
        self.ram_total_MB, self.ram_used_MB = self._get_ram_info_mb()
        self.disk_total_GB, self.disk_used_GB = self._get_disk_info_gb()
        self.cpu_usage : float = self._get_cpu_usage()
        self.serial_number = self._get_machine_serial_number()

    def _get_machine_serial_number(self) -> str:
        """Returns the machine's serial number"""
        if platform.system() == 'Windows':
            try:
                computer = wmi.WMI()
                bios = computer.Win32_BIOS()[0]
                return bios.SerialNumber.strip() if bios.SerialNumber else "N/A"
            except Exception:
                return "N/A"
        else:
            return "N/A"

    def _get_ram_info_mb(self) -> Tuple[int, int]:
        """Returns the total and used RAM in MB"""
        ram = psutil.virtual_memory()
        total_ram = ram.total // (1024 * 1024)  # in MB
        used_ram = ram.used // (1024 * 1024)    # in MB
        return total_ram, used_ram

    def _get_disk_info_gb(self) -> Tuple[int, int]:
        """Returns the total and used disk space in GB"""	
        disk = psutil.disk_usage('/')
        disk_size = disk.total // (1024 * 1024 * 1024)  # in GB
        disk_used = disk.used // (1024 * 1024 * 1024)   # in GB
        return disk_size, disk_used

    def _get_cpu_usage(self) -> float:
        """Returns the CPU usage in percentage"""
        return psutil.cpu_percent(interval=0.5, percpu=False)
