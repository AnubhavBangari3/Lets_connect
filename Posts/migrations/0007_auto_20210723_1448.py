# Generated by Django 3.1.2 on 2021-07-23 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0006_auto_20210722_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts'),
        ),
    ]
