# Generated by Django 5.1.2 on 2024-12-09 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_match_away_score_alter_match_home_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='hasTeam',
            field=models.BooleanField(default=False),
        ),
    ]
