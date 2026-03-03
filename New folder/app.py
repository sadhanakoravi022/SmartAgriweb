from flask import Flask, send_from_directory, jsonify, request
from datetime import datetime, timedelta
from pathlib import Path
import random
import os

# ✅ THIS IS THE FIX — gets the folder where app.py is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


# ══════════════════════════════════════════
#  SERVE SmartAgriWeb.html
# ══════════════════════════════════════════

@app.route("/")
def index():
    # ✅ Looks for SmartAgriWeb.html in the SAME folder as app.py
    return send_from_directory(BASE_DIR, "SmartAgriWeb.html")

# ══════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════

def week_labels():
    today = datetime.today()
    return [(today - timedelta(days=6 - i)).strftime("%a") for i in range(7)]

def live_sensor():
    return {
        "temperature":   round(random.uniform(29.0, 33.0), 1),
        "humidity":      random.randint(52, 64),
        "soil_moisture": random.randint(38, 50),
        "timestamp":     datetime.now().strftime("%H:%M:%S"),
    }


# ══════════════════════════════════════════
#  CROP DATABASE
# ══════════════════════════════════════════

CROPS = {
    "tomato":     {"name":"Tomato",     "icon":"🍅","category":"Vegetable",      "water":"35-45 L/day","season":"Summer",      "yield":"25 t/ha", "days":"70-85 days",   "color":"#e74c3c","weekly_water":[38,40,42,41,43,40,39],"tips":["Needs full sun 6-8 hrs","Water at base not leaves","Use calcium-rich fertilizer","Watch for blight after rain"]},
    "potato":     {"name":"Potato",     "icon":"🥔","category":"Root Vegetable", "water":"25-30 L/day","season":"Spring/Fall", "yield":"20 t/ha", "days":"90-120 days",  "color":"#d4a017","weekly_water":[25,27,28,26,29,27,26],"tips":["Needs well-drained soil","Hill up soil as plant grows","Avoid overwatering","Harvest when leaves yellow"]},
    "corn":       {"name":"Corn",       "icon":"🌽","category":"Cereal Grain",   "water":"30-40 L/day","season":"Summer",      "yield":"8 t/ha",  "days":"80-100 days",  "color":"#f5a623","weekly_water":[30,33,35,38,36,34,32],"tips":["Plant in blocks for pollination","Needs nitrogen-rich soil","Irrigate at silking stage","Check for corn earworm"]},
    "wheat":      {"name":"Wheat",      "icon":"🌾","category":"Cereal Grain",   "water":"18-22 L/day","season":"Winter",      "yield":"3.5 t/ha","days":"110-140 days", "color":"#c9a84c","weekly_water":[18,20,21,22,20,19,18],"tips":["Sow in cool weather","Moderate irrigation only","Use phosphorus fertilizer","Watch for rust disease"]},
    "rice":       {"name":"Rice",       "icon":"🍚","category":"Cereal Staple",  "water":"50-60 L/day","season":"Monsoon",     "yield":"4 t/ha",  "days":"100-150 days", "color":"#a8d5a2","weekly_water":[55,58,60,57,56,54,52],"tips":["Needs flooded paddy field","Warm humid climate ideal","Monitor for leaf blast","Drain field 2 weeks before harvest"]},
    "cucumber":   {"name":"Cucumber",   "icon":"🥒","category":"Vegetable",      "water":"28-35 L/day","season":"Summer",      "yield":"18 t/ha", "days":"50-70 days",   "color":"#27ae60","weekly_water":[28,30,32,33,31,30,29],"tips":["Needs trellis support","High water need in summer","Harvest before yellowing","Watch for powdery mildew"]},
    "spinach":    {"name":"Spinach",    "icon":"🥬","category":"Leafy Green",    "water":"20-28 L/day","season":"Cool Season", "yield":"8 t/ha",  "days":"30-50 days",   "color":"#2ecc71","weekly_water":[20,22,24,25,23,21,20],"tips":["Grows best below 24C","Harvest outer leaves first","Avoid overwatering","Short cycle great for rotation"]},
    "onion":      {"name":"Onion",      "icon":"🧅","category":"Bulb Vegetable", "water":"22-28 L/day","season":"Spring",      "yield":"15 t/ha", "days":"90-120 days",  "color":"#9b59b6","weekly_water":[22,24,25,26,25,23,22],"tips":["Reduce water before harvest","Avoid nitrogen late in season","Plant in full sun","Cure bulbs before storage"]},
    "garlic":     {"name":"Garlic",     "icon":"🧄","category":"Bulb Vegetable", "water":"15-20 L/day","season":"Fall/Spring", "yield":"8 t/ha",  "days":"150-180 days", "color":"#95a5a6","weekly_water":[15,17,18,19,18,16,15],"tips":["Plant in fall for spring harvest","Well-drained soil essential","Stop watering 3-4 weeks before harvest","Separate cloves before planting"]},
    "mango":      {"name":"Mango",      "icon":"🥭","category":"Tropical Fruit", "water":"40-50 L/day","season":"Summer",      "yield":"10 t/ha", "days":"100-150 days", "color":"#ff9f43","weekly_water":[40,43,45,47,46,44,42],"tips":["Requires dry spell to flower","Full tropical sun needed","Prune after harvest","Watch for mango hopper pest"]},
    "banana":     {"name":"Banana",     "icon":"🍌","category":"Tropical Fruit", "water":"45-60 L/day","season":"Year-round",  "yield":"30 t/ha", "days":"270-365 days", "color":"#f1c40f","weekly_water":[48,50,52,54,52,50,49],"tips":["Needs lots of potassium","Wind protection important","Remove oldest leaves regularly","Harvest when fingers round out"]},
    "sugarcane":  {"name":"Sugarcane",  "icon":"🎋","category":"Cash Crop",      "water":"60-80 L/day","season":"Year-round",  "yield":"60 t/ha", "days":"280-365 days", "color":"#16a085","weekly_water":[65,68,72,75,73,70,68],"tips":["Heavy feeder use compost","Needs long frost-free season","Harvest at 12-18 months","Ratoon cropping saves cost"]},
    "soybean":    {"name":"Soybean",    "icon":"🌱","category":"Legume",         "water":"20-30 L/day","season":"Summer",      "yield":"2.5 t/ha","days":"80-110 days",  "color":"#27ae60","weekly_water":[20,22,25,28,27,24,22],"tips":["Fixes own nitrogen in soil","Rotate with cereal crops","Monitor for aphids","Harvest when pods rattle"]},
    "carrot":     {"name":"Carrot",     "icon":"🥕","category":"Root Vegetable", "water":"20-25 L/day","season":"Spring/Fall", "yield":"25 t/ha", "days":"70-90 days",   "color":"#e67e22","weekly_water":[20,21,23,24,23,22,21],"tips":["Deep loose soil for long roots","Thin seedlings to avoid crowding","Reduce water near harvest","Avoid fresh manure"]},
    "pepper":     {"name":"Pepper",     "icon":"🌶","category":"Vegetable",      "water":"25-35 L/day","season":"Summer",      "yield":"12 t/ha", "days":"70-90 days",   "color":"#e74c3c","weekly_water":[25,27,30,32,31,29,27],"tips":["Needs warm nights above 18C","Mulch to retain moisture","Stake tall varieties","Harvest green or wait for color"]},
    "grape":      {"name":"Grape",      "icon":"🍇","category":"Fruit Vine",     "water":"30-40 L/day","season":"Summer",      "yield":"8 t/ha",  "days":"150-180 days", "color":"#8e44ad","weekly_water":[30,32,35,37,36,34,32],"tips":["Train on trellis system","Prune hard in winter","Reduce water before harvest","Watch for downy mildew"]},
    "strawberry": {"name":"Strawberry", "icon":"🍓","category":"Berry Fruit",    "water":"20-30 L/day","season":"Spring",      "yield":"15 t/ha", "days":"60-90 days",   "color":"#e84393","weekly_water":[22,24,26,28,26,24,22],"tips":["Use drip irrigation","Mulch with straw to prevent rot","Remove runners for bigger berries","Replant every 3 years"]},
    "watermelon": {"name":"Watermelon", "icon":"🍉","category":"Fruit",          "water":"40-55 L/day","season":"Summer",      "yield":"20 t/ha", "days":"70-90 days",   "color":"#2ecc71","weekly_water":[42,45,48,50,49,46,44],"tips":["Needs 3 months warm weather","Reduce water when fruit ripens","Hollow thump sound means ripe","Needs space to sprawl"]},
}


# ══════════════════════════════════════════
#  API — CROP SEARCH
# ══════════════════════════════════════════

@app.route("/api/crops/search")
def crop_search():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify([])
    results = []
    for key, crop in CROPS.items():
        if q in crop["name"].lower() or q in crop["category"].lower():
            results.append({"key":key,"name":crop["name"],"icon":crop["icon"],"category":crop["category"],"days":crop["days"]})
    return jsonify(results)

@app.route("/api/crops/<crop_key>")
def crop_detail(crop_key):
    crop = CROPS.get(crop_key.lower())
    if not crop:
        return jsonify({"error": f"Crop '{crop_key}' not found"}), 404
    return jsonify({**crop, "key": crop_key.lower()})


# ══════════════════════════════════════════
#  API — HOME
# ══════════════════════════════════════════

@app.route("/api/home/stats")
def home_stats():
    return jsonify({"total_water_used":520,"water_wasted_today":120,"active_crops":4,"alerts_count":2})

@app.route("/api/home/water-usage")
def home_water_usage():
    return jsonify({"labels":week_labels(),"water_used":[340,420,370,400,460,480,520],"water_wasted":[60,80,55,90,100,110,120]})

@app.route("/api/home/alerts")
def home_alerts():
    return jsonify([
        {"type":"warning","title":"Low Water Level",         "message":"Cucumbers tank below 10%",             "time":"09:45 AM"},
        {"type":"danger", "title":"Over-Irrigation Detected","message":"Spinach exceeded daily limit by 25 L","time":"08:12 AM"},
    ])


# ══════════════════════════════════════════
#  API — WATER IRRIGATION
# ══════════════════════════════════════════

@app.route("/api/water/status")
def water_status():
    return jsonify({"soil_moisture":45,"soil_condition":"Optimal","temperature":32,"humidity":60,"rain_expected":False,"irrigation_needed":True,"recommended_time":"Early Morning","today_usage":520,"week_usage":3600})

@app.route("/api/water/weekly")
def water_weekly():
    return jsonify({"labels":week_labels(),"data":[480,510,460,520,540,490,520]})

@app.route("/api/water/start", methods=["POST"])
def water_start():
    return jsonify({"success":True,"message":"Irrigation started!","started_at":datetime.now().strftime("%H:%M:%S")})


# ══════════════════════════════════════════
#  API — ANALYTICS
# ══════════════════════════════════════════

@app.route("/api/analytics/forecast")
def analytics_forecast():
    return jsonify({"labels":week_labels(),"icons":["⛅","🌤","🌥","🌧","🌧","⛅","🌤"],"temps":[24,26,20,13,13,15,18],"wind":"15 km/h NW","humidity":45})

@app.route("/api/analytics/vitals")
def analytics_vitals():
    return jsonify({"avg_soil_moisture":32,"air_temperature":26,"active_alerts":3,"local_alert":"Frost Advisory"})

@app.route("/api/analytics/tasks")
def analytics_tasks():
    return jsonify([{"id":1,"name":"Morning Diagnostics","status":"done"},{"id":2,"name":"Refill Nitrogen Tank","status":"critical"},{"id":3,"name":"Inspect Sensor A","status":"warning"}])

@app.route("/api/analytics/yield")
def analytics_yield():
    return jsonify({"labels":["Wheat","Corn","Soybeans"],"data":[720,640,580],"colors":["#3cb554","#3498db","#f5a623"]})


# ══════════════════════════════════════════
#  API — INVENTORY
# ══════════════════════════════════════════

@app.route("/api/inventory/metrics")
def inventory_metrics():
    return jsonify({"water_efficiency":"1.2 kg/L","operational_cost":"$1,250","disease_risk":"Low (15%)","system_uptime":"99.8%","yield_change":"+3.2%"})

@app.route("/api/inventory/generate-report", methods=["POST"])
def generate_report():
    return jsonify({"success":True,"report_id":f"RPT-{random.randint(1000,9999)}","generated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"message":"Report generated successfully."})


# ══════════════════════════════════════════
#  API — LIVE SENSORS
# ══════════════════════════════════════════

@app.route("/api/sensors/live")
def sensors_live():
    return jsonify(live_sensor())

@app.route("/api/sensors/charts")
def sensors_charts():
    return jsonify({"labels":week_labels(),"temperature":[29,31,32,30,31,32,31],"soil_moisture":[58,55,48,50,45,42,43]})


# ══════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5500)