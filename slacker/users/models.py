from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hipo_django_core.models import AbstractBaseModel
from hipo_django_core.utils import generate_unique_id

from slacker.users.managers import UserManager


def generate_string_unique_id():
    return str(generate_unique_id())


class User(PermissionsMixin, AbstractBaseModel, AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    username = models.CharField(default=generate_string_unique_id, unique=True, max_length=255)

    is_staff = models.BooleanField(default=False, help_text=_("Only staff users can access Django Admin."))

    # Slack
    slack_user_id = models.CharField(max_length=255, blank=True)
    slack_workspace = models.ForeignKey("slack.SlackWorkspace", related_name="users", on_delete=models.CASCADE)

    # Moku
    moku_email = models.EmailField(blank=True)
    moku_password = models.CharField(blank=True, max_length=255)
    moku_api_token = models.CharField(blank=True, max_length=255)
    is_moku_credentials_validated = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.name}"
