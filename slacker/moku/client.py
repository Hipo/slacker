import requests
from datetime import datetime

import pytz
from django.core.exceptions import ValidationError


class MokuClient:
    token = None
    moku_login_url = "https://hipo.getmoku.com/api/auth/login/"
    moku_user_info_url = "https://hipo.getmoku.com/api/auth/user/"

    def __init__(self, api_token):
        self.api_token = api_token

    @classmethod
    def get_api_token(cls, email, password):
        headers = {"Content-Type": "application/json"}
        json = {
            "email": email,
            "password": password,
        }

        response = requests.post(
            url=cls.moku_login_url,
            headers=headers,
            json=json
        )

        if response.status_code != 200:
            raise ValidationError("Credentials are not correct. I'm disappointed.")

        return response.json()["key"]

    def get_user_info(self):
        headers = {"Authorization": f"Token {self.api_token}"}
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
