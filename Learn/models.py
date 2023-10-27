from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Scripts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    idea = models.TextField()
    generated_script = models.TextField()
    quiz = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now)
    episode = models.PositiveIntegerField(default=1)  # Add an episode field

    def __str__(self):
        return self.title
