# Generated by Django 4.2.2 on 2023-07-25 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0031_remove_scripts_episode_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scripts',
            name='episode_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='scripts',
            name='unique_identifier',
            field=models.CharField(default='', max_length=50),
        ),
    ]
