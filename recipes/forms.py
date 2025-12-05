# recipes/forms.py
from django import forms
from .models import Recipe, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'ingredients', 'steps',
            'cooking_time', 'difficulty', 'image', 'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название рецепта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Каждый ингредиент с новой строки'}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Каждый шаг приготовления с новой строки'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'ingredients': 'Ингредиенты',
            'steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления (минуты)',
            'difficulty': 'Сложность',
            'image': 'Изображение',
            'category': 'Категория',
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или ингредиентам'
        }),
        label='Поиск'
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория'
    )
    
    difficulty = forms.ChoiceField(
        choices=[('', 'Любая сложность')] + Recipe.DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Сложность'
    )
    
    max_cooking_time = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Макс. время (мин)'
        }),
        label='Максимальное время приготовления'
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))