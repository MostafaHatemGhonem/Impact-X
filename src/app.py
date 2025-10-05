
from bottle import response
import json
import os
import requests
import math
from calculations import full_impact_calculation
from simulation import generate_map_html, generate_detailed_map_html
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
            # Clean and validate input parameters
            asteroid_name = asteroid_name.replace(" ", "").strip() if asteroid_name else None
            
            # Set default values if not provided
            lat = float(lat) if lat not in (None, "") else 0.0
            long = float(long) if long not in (None, "") else 0.0
            
            # Validate coordinates
            if not (-90 <= lat <= 90 and -180 <= long <= 180):
                return json.dumps({"error": "Invalid coordinates. Latitude must be between -90 and 90, Longitude between -180 and 180"})
    
            # Calculate diameter and velocity based on input parameters
            if asteroid_name and h_value not in (None, "") and velocity not in (None, ""):
                # Calculate diameter from magnitude (H value)
                try:
                    h_value_float = float(h_value)
                    velocity_float = float(velocity)
                    actual_diameter_km = 1329 / math.sqrt(pv) * (10 ** (-0.2 * h_value_float))
                    actual_diameter_m = actual_diameter_km * 1000
                    actual_velocity_ms = velocity_float * 1000  # Convert km/s to m/s
                except (ValueError, TypeError) as e:
                    return json.dumps({"error": f"Invalid numeric input: {str(e)}"})
                    
            elif (not asteroid_name) and (diameter not in (None, "")) and (velocity not in (None, "")):
                # Use user-provided diameter and velocity
                try:
                    actual_diameter_m = float(diameter) * 1000  # Convert km to m
                    actual_velocity_ms = float(velocity) * 1000  # Convert km/s to m/s
                except (ValueError, TypeError) as e:
                    return json.dumps({"error": f"Invalid numeric input: {str(e)}"})
            else:
                return json.dumps({"error": "Missing required parameters. Need either (asteroid_name, h_value, velocity) or (diameter, velocity)."})
    
            # Determine if impact is in ocean or on land
            try:
                location_status = self.check_land_or_water(lat, long, api_key)
                is_ocean = location_status.get("is_ocean", False)
            except Exception as e:
                print(f"Warning: Could not determine land/water status: {str(e)}")
                is_ocean = False  # Default to land if we can't determine

            # Calculate impact effects
            try:
                impact_results = full_impact_calculation(
                    diameter_m=actual_diameter_m,
                    velocity_ms=actual_velocity_ms,
                    is_ocean=is_ocean
                )
                
                # Generate map with damage zones
                map_html = generate_detailed_map_html(
                    latitude=lat,
                    longitude=long,
                    damage_radii_dict=impact_results.get("damage_radii_km", {}),
                    earthquake_magnitude=impact_results.get("earthquake_magnitude", 0)
                )

                # Compile final results
                final_results = {
                    **impact_results,
                    "map_html": map_html,
                    "is_ocean": is_ocean,
                    "status": "success"
                }
                return json.dumps(final_results)
                
            except Exception as e:
                return json.dumps({"error": f"Error in impact calculation: {str(e)}"})
                
#

        except Exception as e:
            return json.dumps({"error": str(e)})