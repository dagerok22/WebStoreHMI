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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    items = models.TextField(default="")
    price = models.IntegerField(default=0)
    ORDER_STATUS = (
        ("processing", "processing"),
        ("dispatched", "dispatched"),
        ("closed", "closed")
    )
    status = models.CharField(max_length=12, choices=ORDER_STATUS, default=ORDER_STATUS[0])
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
