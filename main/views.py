from django.shortcuts import render, get_object_or_404
from .models import Recipe


def home(request):
    recipes = Recipe.objects.all()

    return render(request, 'main/home.html', {
        'recipes': recipes
    })


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(request, 'main/recipe.html', {
        'recipe': recipe
    })