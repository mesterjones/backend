from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

def wind_direction_to_cardinal(degrees):
    directions = ["North", "North-East", "East", "South-East", 
                  "South", "South-West", "West", "North-West"]
    index = round(degrees / 45) % 8  # Divide into 8 sectors
    return directions[index]

@app.route('/api/weather/<location>')
def get_weather(location):
    print("=== Starting weather request ===")
    print(f"Requested location: {location}")
    
    try:
        api_key = os.getenv('API_KEY')
        print(f"API key exists: {api_key is not None}")
        if not api_key:
            print("WARNING: API_KEY is not set in environment variables!")
            return jsonify({'error': 'API key not configured'}), 500
        
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'
        }
        
        print(f"Making request to OpenWeather API...")
        response = requests.get(url, params=params)
        
        print(f"OpenWeather API Response Status: {response.status_code}")
        print(f"OpenWeather API Response: {response.text}")
        
        response.raise_for_status()
        weather_data = response.json()
        
        formatted_response = {
            'temp': round(weather_data['main']['temp']),
            'wind_speed': weather_data['wind']['speed'],
            'wind_gust': weather_data['wind']['gust'],
            'wind_direction': wind_direction_to_cardinal(weather_data['wind']['deg']),
            'description': weather_data['weather'][0]['description'],
            'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M'),
            'clouds': weather_data['clouds']['all'],
            'rain': weather_data['rain']['1h'] if 'rain' in weather_data else None
        }
        print("=== Successfully completed weather request ===")
        return jsonify(formatted_response)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request Exception: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"General Exception: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/weather/coordinates/<lat>/<lon>')
def get_weather_by_coordinates(lat, lon):
    print("=== Starting weather request ===")
    print(f"Requested coordinates: {lat}, {lon}")
    
    try:
        api_key = os.getenv('API_KEY')
        print(f"API key exists: {api_key is not None}")
        if not api_key:
            print("WARNING: API_KEY is not set in environment variables!")
            return jsonify({'error': 'API key not configured'}), 500
        
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': float(lat),
            'lon': float(lon),
            'appid': api_key,
            'units': 'metric'
        }
        
        print(f"Making request to OpenWeather API...")
        response = requests.get(url, params=params)
        
        print(f"OpenWeather API Response Status: {response.status_code}")
        print(f"OpenWeather API Response: {response.text}")
        
        response.raise_for_status()
        weather_data = response.json()
        
        formatted_response = {
            'temp': round(weather_data['main']['temp']),
            'wind_speed': weather_data['wind']['speed'],
            'wind_gust': weather_data['wind']['gust'],
            'wind_direction': wind_direction_to_cardinal(weather_data['wind']['deg']),
            'description': weather_data['weather'][0]['description'],
            'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M'),
            'clouds': weather_data['clouds']['all'],
            'rain': weather_data['rain']['1h'] if 'rain' in weather_data else None
        }
        print("=== Successfully completed weather request ===")
        return jsonify(formatted_response)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request Exception: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"General Exception: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)