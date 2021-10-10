# Generated by Django 3.1.2 on 2021-07-18 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fist_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('cover', models.ImageField(blank=True, upload_to='profile_picture')),
                ('college', models.CharField(max_length=255)),
                ('about', models.TextField(default='Nothing to write', max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='connections', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
