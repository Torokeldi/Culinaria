from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_url')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'ingredients', 'steps')