""" This module provides the OSInfo class that contains the OS information. """

import platform
import time
import psutil

class OSInfo:
    """ The OSInfo class provides the OS information. """

    def __init__(self) -> None:
        self.os_name: str = self._get_os_name()
        self.os_platform: str = self._get_os_paltform()
        self.uptime: str = self._get_system_uptime()

    @staticmethod
    def _get_os_name() -> str:
        """	Returns the OS information """
        return platform.system() + " " + platform.release()
    
    @staticmethod
    def _get_os_paltform() -> str:
        """	Returns the OS platform information """
        return platform.platform()

    @staticmethod
    def _get_system_uptime() -> str:
        """ Returns the system uptime. 
            In windows this method is not accurate, because can return the boot time from the last
            real shutdown and not the fast boot hybernate often enabled by default. """

        uptime_s = int(round(time.time() - psutil.boot_time()))

        uptime_d = uptime_s // (3600 * 24)
        uptime_h = (uptime_s % (3600 * 24)) // 3600
        uptime_m = (uptime_s % 3600) // 60
        uptime_s = uptime_s % 60

        if uptime_d > 0:
            uptime_str = f"{uptime_d}d, {uptime_h:02}:{uptime_m:02}:{uptime_s:02}"
        else:
            uptime_str = f"{uptime_h:02}:{uptime_m:02}:{uptime_s:02}"

        return uptime_str
