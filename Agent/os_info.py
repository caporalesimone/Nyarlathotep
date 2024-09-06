import platform
import time
import psutil

class OSInfo:
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

        uptime_seconds = int(round(time.time() - psutil.boot_time()))

        uptime_days = uptime_seconds // (3600 * 24)
        uptime_hours = (uptime_seconds % (3600 * 24)) // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_seconds = uptime_seconds % 60

        if uptime_days > 0:
            uptime_str = f"{uptime_days}d, {uptime_hours:02}:{uptime_minutes:02}:{uptime_seconds:02}"
        else:
            uptime_str = f"{uptime_hours:02}:{uptime_minutes:02}:{uptime_seconds:02}"

        return uptime_str
