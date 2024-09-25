"""Main file for the agent."""	

import time
from config_file import ConfigFile
from data_pusher import DataPusher
from versions import CLIENT_SW_VERSION

def main():
    """Main function for the agent."""

    print("Starting agent ...")
    print("Software version: " + CLIENT_SW_VERSION)
    config = ConfigFile()
    data = DataPusher(CLIENT_SW_VERSION, config.custom_name, config.remote_server_url)

    while True:
        start_time = time.time()
        data.push_new_data()
        time.sleep(max(0, config.update_interval - (time.time() - start_time)))

if __name__ == "__main__":
    main()
