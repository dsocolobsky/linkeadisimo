from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Publication(models.Model):
    title = models.CharField(blank=False, max_length=128)
    link = models.URLField(blank=True, default="")
    text = models.TextField(blank=True, default="")
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))

    def __str__(self):
        return f"[{self.link}] ({self.text})"


class Comment(MPTTModel):
    text = models.TextField(blank=False, max_length=8192)
    votes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET(None))
    date = models.DateTimeField(default=timezone.now)
    publication = models.ForeignKey(Publication, on_delete=models.SET(None))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.text

    class MPTTMeta:
        order_insertion_by = ['date']
