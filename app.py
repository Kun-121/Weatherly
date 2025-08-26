from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your API keys
MY_API_KEY = "3fc11a9192f64ef3cf2ddbc4497622af"      # Personal OpenWeatherMap key
DEFAULT_API_KEY = "e754727573aac94fc7951de58c50d123"  # Default/fallback key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city, api_key):
    """Fetch weather data for a city using a given API key"""
    url = f"{BASE_URL}q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        
        # Try using your personal API key first
        response = get_weather(city, MY_API_KEY)
        
        # If city not found or API key fails, try the default key
        if response.get("cod") != 200:
            response = get_weather(city, DEFAULT_API_KEY)

        if response.get("cod") != 200:  # Still fails
            weather_data = {"error": response.get("message", "City not found!")}
        else:
            weather_data = {
                "city": response.get("name"),
                "temperature": response["main"].get("temp"),
                "humidity": response["main"].get("humidity"),
                "description": response["weather"][0].get("description"),
            }

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
