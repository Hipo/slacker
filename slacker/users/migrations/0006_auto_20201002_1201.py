# Generated by Django 2.2.13 on 2020-10-02 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_moku_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='moku_status',
            field=models.CharField(blank=True, choices=[('working', 'working'), ('on_break', 'on_break'), ('idle', 'idle')], default='idle', max_length=255),
        ),
    ]
