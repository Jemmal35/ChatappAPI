# Generated by Django 5.1 on 2024-08-18 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_directmessage_receiver_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
