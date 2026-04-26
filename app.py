# ============================================================
# Weather App — app.py
# Built with Gradio + OpenWeatherMap API
# Theme: Dark Navy + Gold Professional
# ============================================================

import gradio as gr
import requests
from datetime import datetime

# ── Configuration ────────────────────────────────────────────
API_KEY = "f8b1245f1f4c2ca9e2b6567a189ab63d"   # <-- paste your key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ── Weather icons map ────────────────────────────────────────
WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
}

# ── Helper functions ─────────────────────────────────────────
def get_weather_icon(condition: str) -> str:
    return WEATHER_ICONS.get(condition, "🌡️")


def celsius_to_fahrenheit(c: float) -> float:
    return round((c * 9 / 5) + 32, 1)


def fetch_current_weather(city: str, unit: str) -> dict:
    """Fetch current weather data from OpenWeatherMap."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_forecast(city: str) -> dict:
    """Fetch 5-day / 3-hour forecast."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 5,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


# ── Main app function ─────────────────────────────────────────
def get_weather(city: str, unit: str) -> tuple[str, str, str]:
    if not city.strip():
        return "⚠️ Please enter a city name.", "", ""

    try:
        data = fetch_current_weather(city, unit)

        name        = data["name"]
        country     = data["sys"]["country"]
        condition   = data["weather"][0]["main"]
        description = data["weather"][0]["description"].title()
        temp_c      = round(data["main"]["temp"], 1)
        feels_c     = round(data["main"]["feels_like"], 1)
        humidity    = data["main"]["humidity"]
        wind_kph    = round(data["wind"]["speed"] * 3.6, 1)
        pressure    = data["main"]["pressure"]
        visibility  = round(data.get("visibility", 0) / 1000, 1)
        sunrise     = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset      = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
        icon        = get_weather_icon(condition)

        if unit == "Fahrenheit (°F)":
            temp_display  = f"{celsius_to_fahrenheit(temp_c)} °F"
            feels_display = f"{celsius_to_fahrenheit(feels_c)} °F"
        else:
            temp_display  = f"{temp_c} °C"
            feels_display = f"{feels_c} °C"

        current_card = f"""
{icon}  **{name}, {country}**
━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature  : {temp_display}
🤔  Feels like   : {feels_display}
☁️  Condition    : {description}
💧  Humidity     : {humidity}%
💨  Wind speed   : {wind_kph} km/h
🔵  Pressure     : {pressure} hPa
👁️  Visibility   : {visibility} km
🌅  Sunrise      : {sunrise}
🌇  Sunset       : {sunset}
"""

        fcast = fetch_forecast(city)
        forecast_lines = ["📅  **Next 15 hours — forecast**\n━━━━━━━━━━━━━━━━━━━━━━━━━━"]

        for item in fcast["list"]:
            t    = datetime.fromtimestamp(item["dt"]).strftime("%a %H:%M")
            tc   = round(item["main"]["temp"], 1)
            cond = item["weather"][0]["main"]
            fi   = get_weather_icon(cond)
            desc = item["weather"][0]["description"].title()

            td = f"{celsius_to_fahrenheit(tc)} °F" if unit == "Fahrenheit (°F)" else f"{tc} °C"
            forecast_lines.append(f"{fi}  {t}  |  {td}  |  {desc}")

        forecast_card = "\n".join(forecast_lines)

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=10/{lat}/{lon}"

        return current_card, forecast_card, map_link

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"❌ City '{city}' not found. Check the spelling.", "", ""
        return f"❌ API error: {e}", "", ""
    except requests.exceptions.ConnectionError:
        return "❌ No internet connection. Please check your network.", "", ""
    except Exception as e:
        return f"❌ Unexpected error: {e}", "", ""


# ── Custom CSS — Dark Navy + Gold Theme ───────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Mono&display=swap');

/* ── Root palette ── */
:root {
    --navy-deep:   #0A0F1E;
    --navy-mid:    #0D1630;
    --navy-card:   #111E3A;
    --navy-border: #1C2E52;
    --gold:        #F0B429;
    --gold-light:  #FFD97D;
    --gold-dim:    #A07820;
    --text-bright: #E8EEF8;
    --text-muted:  #7A8BAD;
    --accent-blue: #3B7DD8;
    --success:     #2DD4A4;
}

/* ── Page background ── */
body, .gradio-container {
    background: var(--navy-deep) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-bright) !important;
}

/* ── Main container ── */
.gradio-container {
    max-width: 780px !important;
    margin: auto !important;
    padding: 24px !important;
}

/* Hide Gradio footer */
footer { display: none !important; }

/* ── Header markdown ── */
.gradio-container h1 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 4px !important;
}

.gradio-container p {
    color: var(--text-muted) !important;
    font-size: 0.95rem !important;
}

/* ── Input / Textbox ── */
input[type="text"], textarea, .gr-textbox textarea, .gr-textbox input {
    background: var(--navy-card) !important;
    border: 1.5px solid var(--navy-border) !important;
    color: var(--text-bright) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    transition: border-color 0.2s;
}

input[type="text"]:focus, textarea:focus {
    border-color: var(--gold) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(240,180,41,0.15) !important;
}

/* ── Labels ── */
label span, .gr-form label, .label-wrap span {
    color: var(--gold-light) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Radio buttons ── */
.gr-radio input[type="radio"] + span,
.gr-radio label {
    color: var(--text-bright) !important;
}

.gr-radio input[type="radio"]:checked + span {
    color: var(--gold) !important;
}

/* ── Primary button ── */
button.primary, .gr-button-primary {
    background: linear-gradient(135deg, var(--gold) 0%, #D4910A 100%) !important;
    color: var(--navy-deep) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    padding: 12px 28px !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(240,180,41,0.3) !important;
}

button.primary:hover, .gr-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(240,180,41,0.45) !important;
}

button.primary:active {
    transform: translateY(0) !important;
}

/* ── Output markdown panels ── */
.gr-markdown, .gr-prose {
    background: var(--navy-card) !important;
    border: 1.5px solid var(--navy-border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    color: var(--text-bright) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.8 !important;
}

.gr-markdown strong {
    color: var(--gold-light) !important;
    font-weight: 600 !important;
}

/* ── Map textbox output ── */
.gr-textbox-readonly textarea, .gr-textbox[readonly] textarea {
    background: var(--navy-card) !important;
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 10px !important;
}

/* ── Block / panel borders ── */
.gr-block, .gr-box, .gr-panel {
    background: var(--navy-mid) !important;
    border: 1px solid var(--navy-border) !important;
    border-radius: 14px !important;
}

/* ── Examples section ── */
.gr-samples table {
    background: var(--navy-card) !important;
    border-radius: 10px !important;
    border: 1px solid var(--navy-border) !important;
}

.gr-samples td, .gr-samples th {
    color: var(--text-bright) !important;
    border-color: var(--navy-border) !important;
    font-family: 'Outfit', sans-serif !important;
}

.gr-samples tr:hover td {
    background: rgba(240,180,41,0.08) !important;
    cursor: pointer;
}

/* ── Scrollbar styling ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy-deep); }
::-webkit-scrollbar-thumb { background: var(--navy-border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }
"""

# ── Gradio UI ─────────────────────────────────────────────────
def build_ui():
    with gr.Blocks(
        title="🌤️ Weather App",
        theme=gr.themes.Base(),   # Base theme — fully overridden by CSS
        css=CUSTOM_CSS,
    ) as demo:

        gr.Markdown(
            """
            # 🌤️ Weather App
            **Real-time weather powered by OpenWeatherMap**  
            Enter any city name to get current conditions and a short forecast.
            """
        )

        with gr.Row():
            city_input = gr.Textbox(
                label="City name",
                placeholder="e.g. Lahore, London, Tokyo …",
                scale=3,
            )
            unit_input = gr.Radio(
                label="Temperature unit",
                choices=["Celsius (°C)", "Fahrenheit (°F)"],
                value="Celsius (°C)",
                scale=1,
            )

        search_btn = gr.Button("🔍  Get Weather", variant="primary", size="lg")

        with gr.Row():
            current_out  = gr.Markdown(label="Current weather")
            forecast_out = gr.Markdown(label="Forecast")

        map_out = gr.Textbox(
            label="📍 View on map",
            interactive=False,
            placeholder="Map link will appear here …",
        )

        gr.Examples(
            examples=[
                ["Karachi",  "Celsius (°C)"],
                ["Lahore",   "Celsius (°C)"],
                ["London",   "Fahrenheit (°F)"],
                ["Tokyo",    "Celsius (°C)"],
                ["New York", "Fahrenheit (°F)"],
            ],
            inputs=[city_input, unit_input],
        )

        search_btn.click(
            fn=get_weather,
            inputs=[city_input, unit_input],
            outputs=[current_out, forecast_out, map_out],
        )
        city_input.submit(
            fn=get_weather,
            inputs=[city_input, unit_input],
            outputs=[current_out, forecast_out, map_out],
        )

    return demo


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    app = build_ui()
    app.launch(share=True)
