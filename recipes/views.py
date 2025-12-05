# recipes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Recipe, Category
from .forms import RecipeForm, SearchForm, CustomUserCreationForm, CustomAuthenticationForm
from django.core.paginator import Paginator

def home(request):
    """Главная страница со списком рецептов"""
    recipes_list = Recipe.objects.all().select_related('author', 'category')
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        recipes_list = recipes_list.order_by('-views')
    else:  # newest
        recipes_list = recipes_list.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(recipes_list, 9)  # 9 рецептов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes/home.html', context)

def recipe_detail(request, recipe_id):
    """Страница отдельного рецепта"""
    recipe = get_object_or_404(Recipe.objects.select_related('author', 'category'), id=recipe_id)
    
    # Увеличиваем счетчик просмотров
    recipe.increment_views()
    
    # Разделяем ингредиенты и шаги на списки
    ingredients_list = recipe.ingredients.strip().split('\n')
    steps_list = recipe.steps.strip().split('\n')
    
    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'steps_list': steps_list,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def add_recipe(request):
    """Добавление нового рецепта"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    context = {'form': form}
    return render(request, 'recipes/add_recipe.html', context)

def search(request):
    """Поиск и фильтрация рецептов"""
    form = SearchForm(request.GET or None)
    recipes = Recipe.objects.all().select_related('author', 'category')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        difficulty = form.cleaned_data.get('difficulty')
        max_cooking_time = form.cleaned_data.get('max_cooking_time')
        
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) | 
                Q(ingredients__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category:
            recipes = recipes.filter(category=category)
        
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        
        if max_cooking_time:
            recipes = recipes.filter(cooking_time__lte=max_cooking_time)
    
    # Пагинация
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'search_performed': request.GET,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes/search.html', context)

# Регистрация и авторизация
def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'recipes/register.html', context)

def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'recipes/login.html', context)

def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')

@login_required
def profile(request):
    """Профиль пользователя"""
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'user_recipes': user_recipes,
        'recipe_count': user_recipes.count(),
    }
    return render(request, 'recipes/profile.html', context)