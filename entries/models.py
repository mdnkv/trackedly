from django.db import models

from django.contrib.auth import get_user_model

from uuid import uuid4

from projects.models import Project

User = get_user_model()


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=255)
    start_date = models.DateField()
    start_time = models.TimeField()
    finish_date = models.DateField()
    finish_time = models.TimeField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='entries', null=True, blank=True)

    class Meta:
        ordering = ['-finish_date', '-finish_time']
