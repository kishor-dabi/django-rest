# Generated by Django 3.0.5 on 2020-04-23 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0005_auto_20200423_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allpermission',
            name='permission_set',
        ),
        migrations.AddField(
            model_name='allpermission',
            name='permission_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='permission_set', to='userrole.PermissionGroup'),
            preserve_default=False,
        ),
    ]
