# Generated by Django 3.0.5 on 2020-04-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0010_auto_20200424_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='permission',
        ),
        migrations.AddField(
            model_name='userrole',
            name='permission',
            field=models.TextField(default='user-read'),
            preserve_default=False,
        ),
    ]
