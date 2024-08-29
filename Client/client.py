import time
from config_file import ConfigFile
from data_pusher import DataPusher
from versions import CLIENT_SW_VERSION

def main():
    config = ConfigFile()
    data = DataPusher(CLIENT_SW_VERSION, config.custom_name, config.remote_server_url)
    
    while True:
        data.push_new_data()
        #print(data.last_json)
        time.sleep(config.update_interval)

if __name__ == "__main__":
    main()
