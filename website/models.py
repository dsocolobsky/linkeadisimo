from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Publication(models.Model):
    title = models.CharField(blank=False, max_length=128)
    link = models.URLField(blank=True, default="")
    text = models.TextField(blank=True, default="", max_length=8192)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None), default=None)

    def __str__(self):
        return f"[{self.link}] ({self.text})"

    def top_level_comments(self):
        return self.comments.filter(parent_comment=None)


class Comment(models.Model):
    text = models.TextField(blank=False, max_length=8192)
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="comments"
    )
    level = models.PositiveSmallIntegerField(default=0)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="comments", blank=True, null=True
    )
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET(None), default=None)

    def __str__(self):
        return self.text

    def delete_comment(self):
        if self.deleted:
            return
        self.deleted = True
        self.text = "Deleted Comment"
        self.save()
        return self
