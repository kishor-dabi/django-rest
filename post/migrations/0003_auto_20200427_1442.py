# Generated by Django 3.0.5 on 2020-04-27 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200427_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='user_locations',
            new_name='user_location',
        ),
    ]
