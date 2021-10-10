# Generated by Django 3.1.2 on 2021-07-21 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Profile', '0002_auto_20210718_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='posts')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_posts', to='Profile.profile')),
                ('liked', models.ManyToManyField(blank=True, related_name='likes', to='Profile.Profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
