from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from slacker.moku.client import MokuClient

import requests
from slacker.users.models import User

SLACK_OAUTH_URL = "https://slack.com/api/oauth.access"
SLACK_OAUTH_SCOPES = "channels:read,chat:write:bot,commands,users.profile:write"

SLACK_COMMAND_HELLO = 'hello'
SLACK_COMMAND_IAM = 'iam'

ALLOWED_COMMANDS = [
    SLACK_COMMAND_HELLO,
    SLACK_COMMAND_IAM,
]

class SlackOAuthView(View):
    """
    Authenticates the workspace, saves or updates internal list of channels
    """
    def get(self, request):
        auth_code = request.GET.get('code')
        
        if not auth_code:
            return render(request, 'slack/authenticate.html', {
                'client_id': settings.SLACK_CLIENT_ID,
                'oauth_scope': SLACK_OAUTH_SCOPES,
            })
        
        response = requests.get(SLACK_OAUTH_URL, params={
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': auth_code,
        }).json()
        
        access_token = response.get('access_token')
        team_id = response.get('team_id')

        if not access_token or not team_id:
            return render(request, 'slack/authenticate.html', {
                'client_id': settings.SLACK_CLIENT_ID,
                'oauth_scope': SLACK_OAUTH_SCOPES,
            })

        User.objects.get_or_create(
            slack_user_id=response["user_id"],
            slack_access_token=response["access_token"],
        )
        
        return render(request, 'slack/success.html')


@method_decorator(csrf_exempt, name='dispatch')
class SlackCommandView(View):
    """
    Handles incoming commands from Slack
    """
    def post(self, request):
        """
        {'token': ['xXUGp4uz5jXEWARaiqwOSpOW'],
        'team_id': ['T025D0M1W'],
        'team_domain': ['hipo'],
        'channel_id': ['C01BAM09N7P'],
        'channel_name': ['slacker'],
        'user_id': ['U1XAH2108'],
        'user_name': ['efe'],
        'command': ['/slacker'],
        'text': ['hello'],
        'api_app_id': ['A01BEN64K6H'],
        'response_url': ['https://hooks.slack.com/commands/T025D0M1W/1404536512737/MUcXMTrhvjU21GhoIXZ0Ci74'],
        'trigger_id': ['1392114339171.2183021064.cded529f7b3f112118fa93953bb4ce62']}
        """
        command = request.POST.get('text').strip()
        username = request.POST.get('user_name')
        user_id = request.POST.get('user_id')

        if command not in ALLOWED_COMMANDS and not request.POST.get('text').startswith("iam"):
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': "Sorry, I don't know this command. Please try one of the allowed commands."
            })
        elif command == SLACK_COMMAND_HELLO:
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': f"Hello, @{username}! Click here and get ready! https://658016995333.ngrok.io/slack/oauth/"
            })
        # elif command == SLACK_COMMAND_IAM:
        elif request.POST.get('text').startswith("iam"):
            credentials = request.POST.get('text').split("|")[-1]
            email, password = credentials.split(":")
            email = email.replace(">", "")

            user = User.objects.get(slack_user_id=user_id)
            user.moku_email = email
            user.moku_password = password
            user.save()

            try:
                moku_api_token = MokuClient.get_api_token(email=user.moku_email, password=user.moku_password)
            except ValidationError as e:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': e.message
                })

            user.moku_api_token = moku_api_token
            user.is_moku_credentials_validated = True
            user.save()

            return JsonResponse({
                'response_type': 'ephemeral',
                'text': f"Thank you, @{username}! Take a break and see what will happen!"
            })
        else:
            return HttpResponse(status=200)
