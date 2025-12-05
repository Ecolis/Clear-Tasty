import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cooking.settings')
django.setup()

from recipes.models import Category

categories = [
    'Завтрак',
    'Обед',
    'Ужин',
    'Десерт',
    'Закуски',
    'Салаты',
    'Супы',
    'Основные блюда',
    'Выпечка',
    'Напитки',
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

print(f"Создано {len(categories)} категорий")