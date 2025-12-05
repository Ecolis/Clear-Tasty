from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от Django

# Моковые данные для демонстрации
SAMPLE_STATS = {
    "total_recipes": 150,
    "categories_distribution": {
        "Завтрак": 35,
        "Обед": 42,
        "Ужин": 28,
        "Десерт": 25,
        "Закуски": 20
    },
    "difficulty_distribution": {
        "easy": 60,
        "medium": 70,
        "hard": 20
    },
    "avg_cooking_time": 45,
    "most_popular_recipe": "Салат Цезарь",
    "last_updated": datetime.now().isoformat()
}

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Возвращает статистику по рецептам"""
    # Можно добавить параметры фильтрации
    category = request.args.get('category', None)
    
    if category:
        # Фильтруем по категории (в реальном приложении здесь была бы БД)
        filtered_stats = {
            "category": category,
            "recipe_count": SAMPLE_STATS["categories_distribution"].get(category, 0),
            "avg_time": SAMPLE_STATS["avg_cooking_time"]
        }
        return jsonify(filtered_stats)
    
    return jsonify(SAMPLE_STATS)

@app.route('/api/stats/recommend', methods=['GET'])
def get_recommendation():
    """Рекомендация рецепта на основе сложности"""
    difficulty = request.args.get('difficulty', 'medium')
    
    recommendations = {
        'easy': ["Омлет с овощами", "Салат из свежих овощей", "Бутерброды"],
        'medium': ["Салат Цезарь", "Паста Карбонара", "Курица гриль"],
        'hard': ["Шоколадный торт", "Лазанья", "Утка по-пекински"]
    }
    
    return jsonify({
        "difficulty": difficulty,
        "recommended_recipes": recommendations.get(difficulty, []),
        "message": f"Рекомендуем эти рецепты для уровня '{difficulty}'"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({
        "status": "healthy",
        "service": "recipe-stats-service",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)