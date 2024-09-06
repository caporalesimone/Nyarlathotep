from typing import List, Dict

import subprocess

class UserInfo:


    # Old method

    # @staticmethod
    # def get_logged_users():
    #     users = []
    #     for user in psutil.users():
    #         username = user.name
    #         logged = True  # TODO: Implement a way to check if user is logged in
    #         login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.started))
    #         users.append({"username": username, "logged": logged, "login_time": login_time})
    #     return users
    

    @staticmethod
    def get_logged_users() -> List[Dict[str, str]]:
        # Alternative command qwinsta
        result = subprocess.run(['query', 'user'], capture_output=True, text=True) 

        # Seems it always return 1. why?
        # if result.returncode != 0:
        #     print(result.returncode)
        #     print("Error on command 'query user'.")
        #     return
    
        #print(result.stdout) # debug print

        # parsing result
        lines = result.stdout.splitlines()
        users = []
    
        # Skip first line, which is the header
        for line in lines[1:]:  
            parts = line.split()
            if len(parts) >= 3:
                username = parts[0].lstrip('>').upper()
                session_name = parts[1]
                logged = True if session_name.lower() in ['console'] else False
                session_id = parts[2]
                status = parts[3]
                idle_time = parts[4]
                login_time = parts[5] + ' ' + parts[6]
                users.append({"username": username, "session_name": session_name, "session_id": session_id, "status": status, "idle_time": idle_time, "login_time": login_time, "logged": logged})
        return users

