import requests
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hipo_django_core.models import AbstractBaseModel
from hipo_django_core.utils import generate_unique_id

from slacker.users.managers import UserManager
from slacker.users.constants import MOKU_STATUS_CHOICES, MOKU_STATUS_IDLE


def generate_string_unique_id():
    return str(generate_unique_id())


class User(PermissionsMixin, AbstractBaseModel, AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    username = models.CharField(default=generate_string_unique_id, unique=True, max_length=255)

    is_staff = models.BooleanField(default=False, help_text=_("Only staff users can access Django Admin."))

    # Slack
    slack_user_id = models.CharField(max_length=255, blank=True)
    slack_access_token = models.CharField(max_length=255, blank=True)
    replaced_slack_status_emoji = models.CharField(max_length=255, blank=True)
    replaced_slack_status_description = models.CharField(max_length=255, blank=True)

    # Moku
    moku_email = models.EmailField(blank=True)
    moku_password = models.CharField(blank=True, max_length=255)
    moku_api_token = models.CharField(blank=True, max_length=255)
    is_moku_credentials_validated = models.BooleanField(default=False)
    moku_status = models.CharField(choices=MOKU_STATUS_CHOICES, max_length=255, blank=True, default=MOKU_STATUS_IDLE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.name}"

    def set_slack_status(self, description, emoji):
        url = "https://slack.com/api/users.profile.set"
        payload = {
            "profile": {
                "status_text": description,
                "status_emoji": emoji,
                "status_expiration": 0
            }
        }
        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.slack_access_token}"})
        return response
