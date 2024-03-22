from django.db import models

from django.contrib.auth import get_user_model

from uuid import uuid4

User = get_user_model()


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-created_at']
