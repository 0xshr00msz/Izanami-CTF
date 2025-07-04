# Generated by Django 5.2.3 on 2025-06-16 07:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreboardEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('last_solve_time', models.DateTimeField(blank=True, null=True)),
                ('rank', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scoreboard_entry', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Scoreboard Entries',
                'ordering': ['-score', 'last_solve_time'],
            },
        ),
    ]
