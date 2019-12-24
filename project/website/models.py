from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)

class Publication(models.Model):
    is_text = models.BooleanField()
    link = models.URLField()
    text = models.TextField()
    votes = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))
