# Generated by Django 4.2.7 on 2023-11-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_app', '0002_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
