from django.db import models


# Create your models here.
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
