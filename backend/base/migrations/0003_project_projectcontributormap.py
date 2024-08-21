# Generated by Django 5.0.7 on 2024-08-13 16:30

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_profile_github_alter_profile_linkedin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('pid', models.UUIDField(default=uuid.uuid3, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('objective', models.TextField(max_length=1000)),
                ('documentation', models.TextField(max_length=50000)),
                ('is_open', models.BooleanField(default=True)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_led', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectContributorMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_super', models.BooleanField(default=False)),
                ('access', models.CharField(choices=[('B', 'Basic'), ('S', 'Scribe'), ('A', 'Admin')], default='B', max_length=1)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to='base.project')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
