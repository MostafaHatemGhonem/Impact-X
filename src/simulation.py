import folium
from folium import plugins


def generate_map_html(latitude, longitude, damage_radius_km):
    """
    Generate an interactive map showing the asteroid impact location and damage radius.
    
    Args:
        latitude (float): Impact location latitude
        longitude (float): Impact location longitude
        damage_radius_km (dict or float): Radius of moderate damage in kilometers
    
    Returns:
        str: HTML string of the generated map
    """
    try:
        # If damage_radius_km is a dict, extract the moderate damage value
        if isinstance(damage_radius_km, dict):
            radius = damage_radius_km.get('moderate_damage_km', 0)
        else:
            radius = damage_radius_km
        
        # Create a map centered on the impact location
        impact_map = folium.Map(
            location=[latitude, longitude],
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        # Add a marker at the impact point
        folium.Marker(
            location=[latitude, longitude],
            popup=f'Impact Point<br>Lat: {latitude}<br>Lon: {longitude}',
            tooltip='Asteroid Impact Location',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(impact_map)
        
        # Add a circle showing the damage radius
        if radius and radius > 0:
            folium.Circle(
                location=[latitude, longitude],
                radius=radius * 1000,  # Convert km to meters
                popup=f'Moderate Damage Radius: {radius:.2f} km',
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.3,
                weight=2
            ).add_to(impact_map)
            
            # Add a second circle for severe damage (smaller radius)
            severe_damage_radius = radius * 0.5
            folium.Circle(
                location=[latitude, longitude],
                radius=severe_damage_radius * 1000,
                popup=f'Severe Damage Radius: {severe_damage_radius:.2f} km',
                color='darkred',
                fill=True,
                fillColor='darkred',
                fillOpacity=0.5,
                weight=2
            ).add_to(impact_map)
        
        # Add fullscreen button
        plugins.Fullscreen(
            position='topright',
            title='Expand map',
            title_cancel='Exit fullscreen',
            force_separate_button=True
        ).add_to(impact_map)
        
        # Add mouse position display
        plugins.MousePosition().add_to(impact_map)
        
        # Generate HTML
        map_html = impact_map._repr_html_()
        
        return map_html
    
    except Exception as e:
        print(f"Error generating map: {e}")
        import traceback
        traceback.print_exc()
        return f"<p>Error generating map: {str(e)}</p>"
def calculate_earthquake_decay_radius(magnitude, target_magnitude):
    """Calculate the radius where earthquake decays to target magnitude."""
    # Simple logarithmic decay model - adjust coefficients as needed
    return 10 ** ((magnitude - target_magnitude) * 0.5) * 10  # in km

def generate_detailed_map_html(latitude, longitude, damage_radii_dict, earthquake_magnitude=7.0):
    try:
        if not isinstance(damage_radii_dict, dict):
            print(f"Warning: damage_radii_dict is not a dict, got {type(damage_radii_dict)}")
            return generate_map_html(latitude, longitude, 0)

        # Create map with OpenStreetMap base layer
        impact_map = folium.Map(location=[latitude, longitude], zoom_start=8, tiles='OpenStreetMap')
        
        # Add the main red danger zone (most prominent feature)
        danger_radius_km = damage_radii_dict.get('severe_damage_km', 0) * 1.5
        if danger_radius_km > 0:
            # Main danger zone (red)
            folium.Circle(
                location=[latitude, longitude],
                radius=danger_radius_km * 1000,  # Convert km to meters
                popup=(
                    f'<b>DANGER ZONE</b><br>'
                    f'<b>Earthquake Magnitude:</b> {earthquake_magnitude:.1f} Richter<br>'
                    f'<b>Radius:</b> {danger_radius_km:.1f} km<br>'
                    f'<b>Effects:</b> Severe structural damage, potential collapses'
                ),
                tooltip='Extreme Danger Area - Evacuation Recommended',
                color='#ff0000',  # Bright red
                fill=True,
                fill_color='#ff0000',
                fill_opacity=0.15,
                weight=3
            ).add_to(impact_map)
            
            # Add wind intensity zones
            wind_radius_km = danger_radius_km * 1.8
            folium.Circle(
                location=[latitude, longitude],
                radius=wind_radius_km * 1000,
                popup=(
                    f'<b>HIGH WIND ZONE</b><br>'
                    f'<b>Wind Speed:</b> 200+ km/h<br>'
                    f'<b>Effects:</b> Widespread damage, uprooted trees, structural damage'
                ),
                tooltip='High Wind Zone',
                color='#ffa500',  # Orange
                fill=True,
                fill_color='#ffa500',
                fill_opacity=0.1,
                weight=2,
                dash_array='5, 5'
            ).add_to(impact_map)
            
            # Add moderate impact zone
            mod_radius_km = danger_radius_km * 0.7
            folium.Circle(
                location=[latitude, longitude],
                radius=mod_radius_km * 1000,
                popup=(
                    f'<b>MODERATE IMPACT ZONE</b><br>'
                    f'<b>Effects:</b> Partial building collapse, fires, severe injuries likely'
                ),
                tooltip='Moderate Impact Zone',
                color='#ff4500',  # OrangeRed
                fill=True,
                fill_color='#ff4500',
                fill_opacity=0.25,
                weight=2
            ).add_to(impact_map)

        # Earthquake decay circles
        earthquake_magnitudes_to_show = [6.0, 5.0, 4.0]
        for mag in earthquake_magnitudes_to_show:
            if mag < earthquake_magnitude:
                radius_km = calculate_earthquake_decay_radius(earthquake_magnitude, mag)
                folium.Circle(
                    radius=radius_km * 1000,
                    location=[latitude, longitude],
                    popup=f"Magnitude: {mag:.1f} Richter",
                    tooltip=f"Magnitude: {mag:.1f} Richter",
                    color='purple',
                    fill=True,
                    fillColor='purple',
                    fillOpacity=0.2,
                    weight=1
                ).add_to(impact_map)

        # Impact marker
        folium.Marker(
            location=[latitude, longitude],
            popup=f'<b>Impact Point</b><br>Lat: {latitude}<br>Lon: {longitude}',
            tooltip='Asteroid Impact Location',
            icon=folium.Icon(color='black', icon='warning-sign')
        ).add_to(impact_map)

        # Damage zones
        damage_zones = [
            ('window_breakage_km', 'Window Breakage', 'yellow', 0.1),
            ('moderate_damage_km', 'Moderate Damage', 'orange', 0.2),
            ('severe_damage_km', 'Severe Damage', 'red', 0.4),
            ('total_destruction_km', 'Total Destruction', 'darkred', 0.6)
        ]

        for key, label, color, opacity in reversed(damage_zones):
            if key in damage_radii_dict:
                radius_km = damage_radii_dict[key]
                if isinstance(radius_km, (int, float)) and radius_km > 0:
                    folium.Circle(
                        location=[latitude, longitude],
                        radius=radius_km * 1000,
                        popup=f'<b>{label}</b><br>Radius: {radius_km:.2f} km',
                        tooltip=f'{label}: {radius_km:.2f} km',
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=opacity,
                        weight=2
                    ).add_to(impact_map)

        folium.LayerControl().add_to(impact_map)
        plugins.Fullscreen(position='topright').add_to(impact_map)
        plugins.MousePosition().add_to(impact_map)
        plugins.MeasureControl(
            position='topleft',
            primary_length_unit='kilometers',
            secondary_length_unit='miles'
        ).add_to(impact_map)

        return impact_map.get_root().render()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"<p>Error generating map: {str(e)}</p>"


def calculate_affected_area(damage_radius_km):
    """Calculate the affected area in square kilometers."""
    import math
    if isinstance(damage_radius_km, (int, float)) and damage_radius_km > 0:
        return math.pi * (damage_radius_km ** 2)
    return 0


def estimate_population_impact(latitude, longitude, damage_radius_km):
    """
    Placeholder function for estimating population impact.
    
    Args:
        latitude (float): Impact location latitude
        longitude (float): Impact location longitude
        damage_radius_km (float): Damage radius in kilometers
    
    Returns:
        dict: Estimated impact information
    """
    affected_area_km2 = calculate_affected_area(damage_radius_km)
    
    # Average global population density
    avg_pop_density = 60  # people per km²
    estimated_affected = int(affected_area_km2 * avg_pop_density)
    
    return {
        "affected_area_km2": round(affected_area_km2, 2),
        "estimated_affected_population": estimated_affected,
        "note": "This is a rough estimate based on average global population density"
    }