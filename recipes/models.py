# recipes/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.TextField(verbose_name="Ингредиенты", help_text="Каждый ингредиент с новой строки")
    steps = models.TextField(verbose_name="Шаги приготовления", help_text="Каждый шаг с новой строки")
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (минуты)",
        validators=[MinValueValidator(1)]
    )
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name="Сложность"
    )
    image = models.ImageField(
        upload_to='recipes/%Y/%m/%d/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Категория"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])