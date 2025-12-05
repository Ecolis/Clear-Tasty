# recipes/admin.py
from django.contrib import admin
from .models import Category, Recipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'cooking_time', 'difficulty', 'views', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['title', 'description', 'ingredients']
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'image')
        }),
        ('Детали рецепта', {
            'fields': ('ingredients', 'steps', 'cooking_time', 'difficulty')
        }),
        ('Мета-информация', {
            'fields': ('author', 'views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 20
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новый рецепт
            obj.author = request.user
        super().save_model(request, obj, form, change)