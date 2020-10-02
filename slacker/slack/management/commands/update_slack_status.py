from datetime import datetime
from time import sleep

import pytz
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from slacker.moku.client import MokuClient
from slacker.users.models import User
from slacker.users.constants import MOKU_STATUS_ON_BREAK, MOKU_STATUS_WORKING


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            for user in User.objects.filter(is_moku_credentials_validated=True).iterator():
                moku_client = MokuClient(api_token=user.moku_api_token)
                moku_user_info = moku_client.get_user_info()

                if moku_user_info["status"] == MOKU_STATUS_ON_BREAK:
                    if moku_user_info["status_end_datetime"]:
                        parsed_datetime = datetime.fromisoformat(moku_user_info["status_end_datetime"].replace("+0000", ""))
                        timezone_offsett = pytz.timezone('Europe/Istanbul').localize(parsed_datetime).strftime("%z")
                        hour = parsed_datetime.hour
                        minute = parsed_datetime.minute
                        message = f"will be back at {hour}:{minute} ({timezone_offsett})."
                    else:
                        message = f"on the break."

                    user.set_slack_status(
                        description=message,
                        emoji=":coffee:"
                    )
                elif moku_user_info["status"] == MOKU_STATUS_WORKING:
                    user.set_slack_status(
                        description="",
                        emoji=""
                    )

            sleep(3)
