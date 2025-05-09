from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from uuid import uuid4

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["scrapping"]
collection = db["scrap_details"]

# API endpoints
COUNTRIES_API = "https://countriesnow.space/api/v0.1/countries"
STATES_API = "https://countriesnow.space/api/v0.1/countries/states"
CITIES_API = "https://countriesnow.space/api/v0.1/countries/state/cities"

@app.route('/')
def index():
    response = requests.get(COUNTRIES_API)
    countries = response.json().get("data", []) if response.status_code == 200 else []
    country_names = sorted([country["country"] for country in countries])
    return render_template("index.html", countries=country_names)

@app.route('/get_states', methods=['POST'])
def get_states():
    country = request.json.get("country")
    if not country:
        return jsonify({"states": []})
    response = requests.post(STATES_API, json={"country": country})
    states = response.json().get("data", {}).get("states", []) if response.status_code == 200 else []
    state_names = [state["name"] for state in states]
    return jsonify({"states": state_names})

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    try:
        data = request.get_json()
        country = data.get('country')
        selected_states = data.get('states', [])
        categories = data.get('categories', [])

        grouped_data = []

        for state in selected_states:
            city_response = requests.post(CITIES_API, json={"country": country, "state": state})
            if city_response.status_code != 200:
                continue
            cities = city_response.json().get("data", [])
            grouped_data.append({
                "state": state,
                "cities": list(set(cities)),  # remove duplicates if any
                "categories": categories
            })

        doc = {
            "id": str(uuid4()),
            "country": country,
            "data": grouped_data
        }

        collection.insert_one(doc)

        return jsonify({
            "message": "Grouped data inserted successfully.",
            "id": doc["id"],
            "summary": doc["data"]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/get_cities_by_country', methods=['POST'])
def get_cities_by_country():
    try:
        data = request.get_json()
        country = data.get('country')
        records = []

        response = requests.post(STATES_API, json={"country": country})
        states = response.json().get("data", {}).get("states", [])

        for state_obj in states:
            state = state_obj["name"]
            city_response = requests.post(CITIES_API, json={"country": country, "state": state})
            if city_response.status_code == 200:
                cities = city_response.json().get("data", [])
                for city in cities:
                    records.append({
                        "country": country,
                        "state": state,
                        "city": city
                    })

        return jsonify({ "records": records })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({ "error": str(e) }), 500
    

if __name__ == '__main__':
    app.run(debug=True)
