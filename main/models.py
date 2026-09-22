from django.db import models
from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    emoji = models.CharField(max_length=10, blank=True)
    image_url = models.URLField(blank=True, null=True)
    ingredients = models.TextField()
    steps = models.TextField()

    def __str__(self):
        return self.name