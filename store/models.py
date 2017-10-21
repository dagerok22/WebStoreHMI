import json

from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    price = models.IntegerField(default=50)
    content = models.TextField()
    number = models.IntegerField()

    def __str__(self):
        return self.title

    def get_short_content(self):
        return self.content[:500]


class Bucket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    items = models.TextField(default="")

    def __len__(self):
        return len(list(json.loads(self.items)))
