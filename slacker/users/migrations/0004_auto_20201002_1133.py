# Generated by Django 2.2.13 on 2020-10-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_slack_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='replaced_slack_status_description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='replaced_slack_status_emoji',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
