from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Recipe


def index(request):
    query = request.GET.get('q', '').strip()

    if query:
        recipes = Recipe.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(steps__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()

    return render(request, 'main/home.html', {
        'recipes': recipes,
        'query': query,
    })


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(request, 'main/recipe.html', {
        'recipe': recipe,
    })