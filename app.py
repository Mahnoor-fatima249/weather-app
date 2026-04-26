import gradio as gr
import requests
from datetime import datetime

# API Configuration
API_KEY = "f8b1245f1f4c2ca9e2b6567a189ab63d"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# CSS file ko read karne ka function
def load_css():
    with open("style.css", "r") as f:
        return f.read()

# Weather Logic Functions
def get_weather_icon(condition):
    icons = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Snow": "❄️", "Mist": "🌫️"}
    return icons.get(condition, "🌡️")

def get_weather(city, unit):
    if not city.strip():
        return "⚠️ Please enter a city name.", "", ""
    try:
        # Current Weather
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        data = requests.get(BASE_URL, params=params).json()
        
        name = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        icon = get_weather_icon(data["weather"][0]["main"])
        
        res = f"## {icon} {name}\n**Temp:** {temp}°C\n**Status:** {desc}"
        return res, "Forecast details...", f"https://www.openstreetmap.org"
    except Exception as e:
        return f"❌ Error: {e}", "", ""

# Building UI
with gr.Blocks(css=load_css()) as demo:
    # HTML file include karna
    with open("index.html", "r") as f:
        gr.HTML(f.read())
        
    with gr.Row():
        city_input = gr.Textbox(label="City name", placeholder="Lahore, London...")
        unit_input = gr.Radio(choices=["Celsius (°C)", "Fahrenheit (°F)"], value="Celsius (°C)")
    
    search_btn = gr.Button("🔍 Get Weather", variant="primary")
    
    with gr.Row():
        current_out = gr.Markdown()
        forecast_out = gr.Markdown()
        
    search_btn.click(get_weather, [city_input, unit_input], [current_out, forecast_out])

if __name__ == "__main__":
    demo.launch()
