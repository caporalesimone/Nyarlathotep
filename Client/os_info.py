import platform

class OSInfo:
    def __init__(self) -> None:
        self.os_name: str = self._get_os_name()

    def _get_os_name(self) -> str:
        """	Returns the OS information """
        return platform.system() + " " + platform.release()