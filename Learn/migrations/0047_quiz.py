# Generated by Django 4.2.2 on 2023-07-28 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learn', '0046_delete_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('generated_script', models.TextField()),
                ('question', models.CharField(max_length=500)),
                ('choice_a', models.CharField(max_length=200)),
                ('choice_b', models.CharField(max_length=200)),
                ('choice_c', models.CharField(max_length=200)),
                ('choice_d', models.CharField(max_length=200)),
                ('correct_answer', models.CharField(max_length=1)),
            ],
        ),
    ]