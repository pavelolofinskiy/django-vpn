# Generated by Django 4.2.7 on 2023-11-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_app', '0004_usersite_usersitetraffic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_sites',
            field=models.ManyToManyField(blank=True, to='vpn_app.usersite'),
        ),
    ]
