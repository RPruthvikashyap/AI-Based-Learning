# Generated by Django 4.2.2 on 2023-07-25 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0030_scripts_unique_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scripts',
            name='episode_number',
        ),
        migrations.RemoveField(
            model_name='scripts',
            name='unique_identifier',
        ),
    ]