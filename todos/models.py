from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('PLANNING', 'Planning'),
        ('ONGOING', 'Ongoing'),
        ('CLOSED', 'Closed'),
    ]

    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_todos')
    assigned_users = models.ManyToManyField(User, blank=True, related_name='assigned_todos')

    def __str__(self):
        return f"[{self.status}] {self.text[:50]}"


class AuthLog(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        state = "SUCCESS" if self.successful else "FAILURE"
        return f"{self.timestamp} - {self.username} - {state}"
