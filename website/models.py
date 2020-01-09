from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Publication(models.Model):
    title = models.CharField(blank=False, max_length=128)
    link = models.URLField(blank=True, default="")
    text = models.TextField(blank=True, default="")
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))

    def __str__(self):
        return f"[{self.link}] ({self.text})"


class Comment(models.Model):
    text = models.TextField(blank=False, max_length=8192)
    votes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))
    publication = models.ForeignKey(Publication, on_delete=models.SET(None))
    parent = models.ForeignKey('self', on_delete=models.SET(None), blank=True, null=True, default=None)

    def __str__(self):
        return self.text
