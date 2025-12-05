from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def get_season(month):
    """Определяет сезон по месяцу"""
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

WEATHER_DATA = {
    "Moscow": {"temp": 15, "condition": "sunny"},
    "Saint Petersburg": {"temp": 12, "condition": "cloudy"},
    "Sochi": {"temp": 22, "condition": "sunny"}
}

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Moscow')
    
    weather = WEATHER_DATA.get(city, {
        "temp": random.randint(-10, 30),
        "condition": random.choice(["sunny", "cloudy", "rainy", "snowy"])
    })
    
    return jsonify({
        "city": city,
        "temperature": weather["temp"],
        "condition": weather["condition"],
        "season": get_season(datetime.now().month),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "weather"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)