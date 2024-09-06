import psutil
import time
from typing import List

class UserInfo:

    @staticmethod
    def get_logged_users():
        users = []
        for user in psutil.users():
            username = user.name
            logged = True  # TODO: Implement a way to check if user is logged in
            login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.started))
            users.append({"username": username, "logged": logged, "login_time": login_time})
        return users