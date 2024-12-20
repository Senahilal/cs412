# Generated by Django 5.1.2 on 2024-12-06 00:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='away_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='MatchRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_receiver', to='project.manager')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_sender', to='project.manager')),
            ],
        ),
    ]
