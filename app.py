from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/weather/<location>')
def get_weather(location):
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        # Debug print to check if API key is loaded
        print(f"Using API key: {api_key}")
        
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'
        }
        
        # Debug print the full URL (without API key)
        print(f"Requesting URL: {url}")
        
        response = requests.get(url, params=params)
        
        # Debug print the response
        print(f"OpenWeather API Response Status: {response.status_code}")
        print(f"OpenWeather API Response: {response.text}")
        
        response.raise_for_status()
        weather_data = response.json()
        
        formatted_response = {
            'temp': round(weather_data['main']['temp']),
            'wind': round(weather_data['wind']['speed']),
            'description': weather_data['weather'][0]['description']
        }
        return jsonify(formatted_response)
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")
        return jsonify({'error': f'Weather API error: {str(e)}'}), 500
    except Exception as e:
        print(f"General Exception: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)