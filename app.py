from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Enable CORS for your GitHub Pages domain
CORS(app, origins=['https://mesterjones.github.io', 'http://localhost:5173'])

@app.route('/api/weather/<location>')
def get_weather(location):
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather',
            params={
                'q': location,
                'appid': api_key
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)