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

# Exemple of output

#  NOMEUTENTE            NOMESESSIONE       ID  STATO   INATTIVITÀ ACCESSO
# >a11111a               rdp-tcp#87          2  Attivo          .  02/09/2024 09:47
#  c22222c                                   3  Disc      1+03:52  05/09/2024 12:51
#  d33333d                                   4  Disc        23:34  05/09/2024 17:08

        # Skip first line, which is the header
        for line in lines[1:]:  
            parts = line.split()

            if len(parts) >= 6:
                idx = 0
                username = parts[idx].lstrip('>').upper()
                idx += 1

                if len(parts) == 7:
                    session_name = parts[idx]
                    logged = True
                    idx += 1
                else:
                    session_name = ''
                    logged = False

                session_id = parts[idx]

                idx += 1
                status = parts[idx]

                idx += 1
                idle_time = parts[idx]

                idx += 1
                login_time = parts[idx] + ' ' + parts[idx + 1]

                idx += 2
                users.append({"username": username, "session_name": session_name, "session_id": session_id, "status": status, "idle_time": idle_time, "login_time": login_time, "logged": logged})
        return users

