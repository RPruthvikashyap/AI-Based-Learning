# Generated by Django 4.2.2 on 2023-07-20 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0022_delete_mcq'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('choice_1', models.CharField(max_length=100)),
                ('choice_2', models.CharField(max_length=100)),
                ('choice_3', models.CharField(max_length=100)),
                ('choice_4', models.CharField(max_length=100)),
                ('correct_choice', models.CharField(max_length=100)),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learn.scripts')),
            ],
        ),
    ]
