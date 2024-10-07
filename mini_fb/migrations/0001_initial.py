# Generated by Django 5.1.1 on 2024-10-07 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('city', models.TextField()),
                ('email', models.TextField()),
                ('image_url', models.URLField(blank=True)),
            ],
        ),
    ]
