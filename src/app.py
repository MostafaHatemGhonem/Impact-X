
from bottle import response
import json
import os
import requests
import math
from calculations import full_impact_calculation
from simulation import generate_map_html
# For local development: load environment variables from a .env file.
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENCAGE_API_KEY")
if not api_key:
    raise ValueError("❌ Missing OPENCAGE_API_KEY in .env file")


pv = 0.15
D = 1329

webPath = os.path.abspath("web")

class Api():
    def get_asteroid_list(self):
        url = "https://ssd-api.jpl.nasa.gov/cad.api"
        params = {
            "dist-min": "0.01",
            "dist-max": "0.05",
            "nea": "true",
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch asteroid list: {response.status_code}"})

        data = response.json()

        if "data" not in data or "fields" not in data:
            return json.dumps({"error": "No asteroid data found in NASA API response."})

        fields = data["fields"]
        des_index = fields.index("des")
        h_index = fields.index("h")
        v_inf_index = fields.index("v_inf")

        asteroid_info = []
        for item in data["data"]:
            if item[h_index] not in (None, "") and item[v_inf_index] not in (None, ""):
                asteroid_info.append({
                    "name": item[des_index],
                    "h": item[h_index],
                    "v_inf": item[v_inf_index]
                })


        return json.dumps(asteroid_info)

    def check_land_or_water(self,lat,lon,api_key):
        """
        land or water by long and lat 
        """
        url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            return {"status": "error", "message": f"API request failed: {response.status_code}"}
        
        data = response.json()

        if not data["results"]:
            return {"status": "unknown", "message": "No results from API"}
        
        components = data["results"][0].get("components", {})
        
        if "country" in components:
            return {
                "is_ocean": False
            }
        else:
            return {
                "is_ocean": True
            }

    def run_simulation(
    self,
    asteroid_name=None,
    diameter=None,
    velocity=None,
    lat=None,
    long=None,
    h_value=None,
    v_inf_value=None
):  
        try:
            asteroid_name = asteroid_name.replace(" ", "").strip() if asteroid_name else None
            lat = float(lat) if lat not in (None, "") else 0.0
            long = float(long) if long not in (None, "") else 0.0
    
            if asteroid_name and h_value not in (None, "") and velocity not in (None, ""):
                # Calculate diameter from magnitude
                actual_diameter_km = 1329 / math.sqrt(pv) * (10 ** (-0.2 * float(h_value)))
                actual_diameter_m = actual_diameter_km * 1000
                actual_velocity_ms = float(velocity) * 1000
            elif (not asteroid_name) and (diameter not in (None, "")) and (velocity not in (None, "")):
                # If the user entered the diameter and speed himself
                actual_diameter_m = float(diameter) * 1000
                actual_velocity_ms = float(velocity) * 1000
            else:
                return json.dumps({"error": "Invalid input parameters"})
    
            # Determine whether the location is ocean or land
            # Determine land/ocean
            location_status = self.check_land_or_water(lat, long, api_key)
            is_ocean = location_status["is_ocean"]

            # Call full impact calculation
            impact_results = full_impact_calculation(
                diameter_m=actual_diameter_m,
                velocity_ms=actual_velocity_ms,
                is_ocean=is_ocean
            )

            # Generate map HTML
            map_html = generate_map_html(
                lat,
                long,
                impact_results["damage_radii_km"]
            )

            # Compile results for frontend
            final_results = {**impact_results, "map_html": map_html, "is_ocean": is_ocean}
            return json.dumps(final_results)
#

        except Exception as e:
            return json.dumps({"error": str(e)})