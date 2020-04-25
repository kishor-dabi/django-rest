# Generated by Django 3.0.5 on 2020-04-23 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_group_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'permission_group',
            },
        ),
        migrations.CreateModel(
            name='AllPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=100)),
                ('permission_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userrole.PermissionGroup')),
            ],
            options={
                'db_table': 'all_permissions',
            },
        ),
    ]