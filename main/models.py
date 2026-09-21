from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    emoji = models.CharField(max_length=10, default='🍴')
    ingredients = models.TextField()
    steps = models.TextField()

    def __str__(self):
        return self.name