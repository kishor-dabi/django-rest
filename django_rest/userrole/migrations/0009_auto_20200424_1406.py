# Generated by Django 3.0.5 on 2020-04-24 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0008_auto_20200423_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allpermission',
            name='permission_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permission_set', to='userrole.PermissionGroup'),
        ),
    ]
