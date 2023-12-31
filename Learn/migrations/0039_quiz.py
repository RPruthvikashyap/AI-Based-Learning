# Generated by Django 4.2.2 on 2023-07-27 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0038_delete_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('generated_script', models.TextField()),
                ('question', models.CharField(max_length=500)),
                ('choices', models.TextField()),
                ('correct_answer', models.CharField(max_length=200)),
            ],
        ),
    ]
