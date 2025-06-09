from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_nws_forecast(lat, lon):
    try:
        point_url = f"https://api.weather.gov/points/{lat},{lon}"
        point_data = requests.get(point_url).json()
        forecast_url = point_data['properties']['forecast']
        forecast_data = requests.get(forecast_url).json()
        return forecast_data['properties']['periods']
    except Exception as e:
        print(f"Error getting NWS data: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    forecast = []
    lat = lon = ""
    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        forecast = get_nws_forecast(lat, lon)
    return render_template("index.html", forecast=forecast, lat=lat, lon=lon)

if __name__ == "__main__":
    app.run(debug=True)
