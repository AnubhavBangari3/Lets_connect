# Generated by Django 3.1.2 on 2021-07-18 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fist_name',
            new_name='first_name',
        ),
    ]
