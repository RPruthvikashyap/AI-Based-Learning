# Generated by Django 4.2.2 on 2023-07-27 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0039_quiz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='choices',
            new_name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='question',
        ),
    ]
