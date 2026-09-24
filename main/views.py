from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Recipe

from django.core.paginator import Paginator

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

    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/home.html', {
        'recipes': page_obj,
        'page_obj': page_obj,
        'query': query,
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Получаем рецепты в том же порядке, что и на главной
    recipes = list(Recipe.objects.all().order_by('id'))

    current_index = next(
        (i for i, item in enumerate(recipes) if item.id == recipe.id),
        None
    )

    previous_recipe = None
    next_recipe = None

    if current_index is not None:
        if current_index > 0:
            previous_recipe = recipes[current_index - 1]

        if current_index < len(recipes) - 1:
            next_recipe = recipes[current_index + 1]

    return render(request, 'main/recipe.html', {
        'recipe': recipe,
        'previous_recipe': previous_recipe,
        'next_recipe': next_recipe,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'main/regAuth.html', {
                'login_error': 'Введите имя пользователя и пароль.'
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'main/regAuth.html', {
            'login_error': 'Неверное имя пользователя или пароль.'
        })

    return render(request, 'main/regAuth.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username or not email or not password or not password_confirm:
            return render(request, 'main/regAuth.html', {
                'register_error': 'Заполните все поля.'
            })

        if password != password_confirm:
            return render(request, 'main/regAuth.html', {
                'register_error': 'Пароли не совпадают.'
            })

        if len(password) < 8:
            return render(request, 'main/regAuth.html', {
                'register_error': 'Пароль должен содержать минимум 8 символов.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'main/regAuth.html', {
                'register_error': 'Пользователь с таким именем уже существует.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'main/regAuth.html', {
                'register_error': 'Пользователь с таким email уже существует.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('home')

    return render(request, 'main/regAuth.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def categories(request):
    return render(request, "main/categories.html")

@login_required(login_url='login')
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        emoji = request.POST.get('emoji', '').strip()
        ingredients = request.POST.get('ingredients', '').strip()
        steps = request.POST.get('steps', '').strip()

        if not name or not description or not category or not ingredients or not steps:
            return render(request, 'main/add_recipe.html', {
                'error': 'Заполните все обязательные поля.',
                'name': name,
                'description': description,
                'category': category,
                'image_url': image_url,
                'emoji': emoji,
                'ingredients': ingredients,
                'steps': steps,
            })

        # ИСПРАВЛЕНО: Теперь обязательно передается author=request.user
        Recipe.objects.create(
            author=request.user,
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            emoji=emoji or '🍲',
            ingredients=ingredients,
            steps=steps,
        )

        return redirect('profile') # Перенаправляем в профиль, чтобы увидеть добавленный рецепт

    return render(request, 'main/add_recipe.html')

@login_required(login_url='login')
def profile(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'main/profile.html', {
        'recipes': recipes,
    })
