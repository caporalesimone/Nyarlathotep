""" This module reads and writes the configuration file for the client. """

import os
from configparser import ConfigParser

CONFIG_FILE = 'config.ini'

# Default values
DEFAULT_CUSTOM_NAME = "WORKSTATION"
DEFAULT_UPDATE_INTERVAL = 30  # in seconds
DEFAULT_REMOTE_SERVER_URL = "http://localhost:8080/client_update"

class ConfigFile:
    """ConfigFile class to read and write the configuration file for the client."""	

    def __init__(self) -> None:
        config = ConfigParser()

        if not os.path.exists(CONFIG_FILE):
            config['SETTINGS'] = {
                'CUSTOM_NAME': DEFAULT_CUSTOM_NAME,
                'UPDATE_INTERVAL': str(DEFAULT_UPDATE_INTERVAL),
                'REMOTE_SERVER_URL': DEFAULT_REMOTE_SERVER_URL
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            print(f"Config file created with default values at {CONFIG_FILE}")

        config.read(CONFIG_FILE)

        if not config.has_option('SETTINGS', 'CUSTOM_NAME'):
            config.set('SETTINGS', 'CUSTOM_NAME', DEFAULT_CUSTOM_NAME)
            updated = True
        else:
            updated = False

        if not config.has_option('SETTINGS', 'UPDATE_INTERVAL'):
            config.set('SETTINGS', 'UPDATE_INTERVAL', str(DEFAULT_UPDATE_INTERVAL))
            updated = True

        if not config.has_option('SETTINGS', 'REMOTE_SERVER_URL'):
            config.set('SETTINGS', 'REMOTE_SERVER_URL', DEFAULT_REMOTE_SERVER_URL)
            updated = True

        if updated:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            print(f"Config file updated with missing default values at {CONFIG_FILE}")

        self.custom_name = config.get('SETTINGS', 'CUSTOM_NAME')
        self.update_interval = config.getint('SETTINGS', 'UPDATE_INTERVAL')
        self.remote_server_url = config.get('SETTINGS', 'REMOTE_SERVER_URL')

        print(f"Custom Name: {self.custom_name}")
        print(f"Update Interval: {self.update_interval}")
        print(f"Remote Server URL: {self.remote_server_url}")
