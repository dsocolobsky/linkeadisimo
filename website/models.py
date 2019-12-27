from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Publication(models.Model):
    is_text = models.BooleanField()
    title = models.CharField(blank=False,max_length=128)
    link = models.URLField(blank=True, default="")
    text = models.TextField(blank=True, default="")
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))

    def __str__(self):
        return (self.text if self.is_text else self.link)
