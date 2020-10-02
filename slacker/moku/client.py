import requests
from datetime import datetime

import pytz


class MokuClient:
    token = None
    moku_login_url = "https://hipo.getmoku.com/api/auth/login/"
    moku_user_info_url = "https://hipo.getmoku.com/api/auth/user/"

    def __init__(self, email, password):
        self.login(email, password)

    def login(self, email, password):
        headers = {"Content-Type": "application/json"}
        json = {
            "email": email,
            "password": password,
        }

        response = requests.post(
            url=self.moku_login_url,
            headers=headers,
            json=json
        ).json()

        self.token = response["key"]

    def get_user_info(self):
        headers = {"Authorization": f"Token {self.token}"}
        return requests.get(
            url=self.moku_user_info_url,
            headers=headers
        ).json()

    def get_user_status(self):
        user_info = self.get_user_info()
        parsed_datetime = datetime.fromisoformat(user_info["status_end_datetime"].replace("+0000", ""))
        timezone_offsett = pytz.timezone('Europe/Istanbul').localize(parsed_datetime).strftime("%z")
        hour = parsed_datetime.hour
        minute = parsed_datetime.minute
        message = f"will be back at {hour}:{minute} ({timezone_offsett})"
        return {
            "status": user_info["status"],
            "message": message
        }
