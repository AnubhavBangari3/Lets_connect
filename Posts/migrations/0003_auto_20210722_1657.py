# Generated by Django 3.1.2 on 2021-07-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_comment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('like', 'like'), ('unlike', 'unlike')], default='like', max_length=8),
        ),
    ]