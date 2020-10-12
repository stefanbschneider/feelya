from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Label(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField('date tracked', auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
