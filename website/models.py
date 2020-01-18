from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Post(MPTTModel):
    votes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None), default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['votes']

    class Meta:
        abstract = True


class Publication(Post):
    text = models.TextField(blank=True, default="", max_length=8192)
    title = models.CharField(blank=False, max_length=128)
    link = models.URLField(blank=True, default="")
    voters = models.ManyToManyField(User, related_name='pub_voters')

    def __str__(self):
        return f"[{self.link}] ({self.text})"

    class MPTTMeta:
        order_insertion_by = ['-votes']


class Comment(Post):
    text = models.TextField(blank=False, max_length=8192)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments', default=None)
    voters = models.ManyToManyField(User, related_name='com_voters')

    def __str__(self):
        return self.text

    class MPTTMeta:
        order_insertion_by = ['-votes']
