
from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('soups', '🍲 Супы'),
        ('meat', '🍖 Мясные блюда'),
        ('chicken', '🍗 Курица'),
        ('fish', '🐟 Рыба'),
        ('salads', '🥗 Салаты'),
        ('pasta', '🍝 Паста'),
        ('baking', '🍕 Выпечка'),
        ('desserts', '🍰 Десерты'),
        ('breakfast', '🥞 Завтраки'),
        ('drinks', '🥤 Напитки'),
        ('rice', '🍚 Рисовые блюда'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='soups',
    )

    emoji = models.CharField(
        max_length=10,
        blank=True,
    )

    image_url = models.URLField(
        blank=True,
        null=True,
    )

    ingredients = models.TextField()

    steps = models.TextField()

    def save(self, *args, **kwargs):
        if not self.emoji:
            category_emojis = {
                'soups': '🍲',
                'meat': '🍖',
                'chicken': '🍗',
                'fish': '🐟',
                'salads': '🥗',
                'pasta': '🍝',
                'baking': '🍕',
                'desserts': '🍰',
                'breakfast': '🥞',
                'drinks': '🥤',
                'rice': '🍚',
            }

            self.emoji = category_emojis.get(
                self.category,
                '🍲',
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

