# Generated by Django 2.2.8 on 2020-08-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0020_notificationlog_notification_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationlog',
            name='Screen_Name',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='notificationlog',
            name='googleapis_Request_Body',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
