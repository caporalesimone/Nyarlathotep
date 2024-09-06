from typing import Tuple
import psutil

class HardwareInfo:
    def __init__(self) -> None:
        self.ram_total_MB, self.ram_used_MB = self._get_ram_info_MB()
        self.disk_total_GB, self.disk_used_GB = self._get_disk_info_GB()
        self.cpu_usage : float = self._get_cpu_usage()

    def _get_ram_info_MB(self) -> Tuple[int, int]:
        """Returns the total and used RAM in MB"""
        ram = psutil.virtual_memory()
        total_ram = ram.total // (1024 * 1024)  # in MB
        used_ram = ram.used // (1024 * 1024)    # in MB
        return total_ram, used_ram

    def _get_disk_info_GB(self) -> Tuple[int, int]:
        """Returns the total and used disk space in GB"""	
        disk = psutil.disk_usage('/')
        disk_size = disk.total // (1024 * 1024 * 1024)  # in GB
        disk_used = disk.used // (1024 * 1024 * 1024)   # in GB
        return disk_size, disk_used

    def _get_cpu_usage(self) -> float:
        """Returns the CPU usage in percentage"""
        return psutil.cpu_percent(interval=0.5, percpu=False)

