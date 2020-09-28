from django.contrib import admin

from slacker.slack.models import SlackWorkspace, SlackChannel


class SlackWorkspaceAdmin(admin.ModelAdmin):
    pass

class SlackChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlackWorkspace, SlackWorkspaceAdmin)
admin.site.register(SlackChannel, SlackChannelAdmin)
