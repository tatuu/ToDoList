from django.db import models
from django.utils import timezone

class List(models.Model):
    title = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)
    

class Task(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    deadline_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)

# Create your models here.
