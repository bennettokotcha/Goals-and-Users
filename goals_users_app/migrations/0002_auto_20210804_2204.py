# Generated by Django 2.2 on 2021-08-04 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals_users_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_level',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=15, null=True),
        ),
    ]