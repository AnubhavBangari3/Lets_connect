# Generated by Django 3.2.6 on 2021-09-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0014_alter_profile_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover',
            field=models.ImageField(blank=True, default='media/profile_picture/avatar.png', upload_to='profile_picture'),
        ),
    ]