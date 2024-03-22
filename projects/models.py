from django.db import models

from django.contrib.auth import get_user_model

from uuid import uuid4

from customers.models import Customer

User = get_user_model()


class Project(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    is_billable = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-created_at']
