import folium
from folium import plugins
import math


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
        if isinstance(damage_radius_km, dict):
            radius = damage_radius_km.get('moderate_damage_km', 0)
        else:
            radius = damage_radius_km
        
        impact_map = folium.Map(
            location=[latitude, longitude],
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        folium.Marker(
            location=[latitude, longitude],
            popup=f'Impact Point<br>Lat: {latitude}<br>Lon: {longitude}',
            tooltip='Asteroid Impact Location',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(impact_map)
        
        if radius and radius > 0:
            folium.Circle(
                location=[latitude, longitude],
                radius=radius * 1000,
                popup=f'Moderate Damage Radius: {radius:.2f} km',
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.3,
                weight=2
            ).add_to(impact_map)
            
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
        
        plugins.Fullscreen(
            position='topright',
            title='Expand map',
            title_cancel='Exit fullscreen',
            force_separate_button=True
        ).add_to(impact_map)
        
        plugins.MousePosition().add_to(impact_map)
        
        map_html = impact_map.repr_html()
        
        return map_html
    
    except Exception as e:
        print(f"Error generating map: {e}")
        import traceback
        traceback.print_exc()
        return f"<p>Error generating map: {str(e)}</p>"


def calculate_earthquake_decay_radius(magnitude, target_magnitude):
    """Calculate the radius where earthquake decays to target magnitude."""
    return 10 ** ((magnitude - target_magnitude) * 0.5) * 10


def generate_detailed_map_html(latitude, longitude, damage_radii_dict, earthquake_magnitude=7.0):
    try:
        if not isinstance(damage_radii_dict, dict):
            print(f"Warning: damage_radii_dict is not a dict, got {type(damage_radii_dict)}")
            return folium.Map(location=[latitude, longitude], zoom_start=8).get_root().render()

        impact_map = folium.Map(location=[latitude, longitude], zoom_start=8, tiles='OpenStreetMap')
        
        # Collect all circles to be drawn
        all_circles = []

        # Damage zones
        damage_zones = [
            ('total_destruction_km', 'Total Destruction', 'darkred', 0.6),
            ('severe_damage_km', 'Severe Damage', 'red', 0.4),
            ('moderate_damage_km', 'Moderate Damage', 'orange', 0.2),
            ('window_breakage_km', 'Window Breakage', 'yellow', 0.1)
        ]

        for key, label, color, opacity in damage_zones:
            if key in damage_radii_dict:
                radius_km = damage_radii_dict[key]
                if isinstance(radius_km, (int, float)) and radius_km > 0:
                    all_circles.append({
                        'radius_km': radius_km,
                        'popup': f'<b>{label}</b><br>Radius: {radius_km:.2f} km',
                        'tooltip': f'{label}: {radius_km:.2f} km',
                        'color': color,
                        'fill_color': color,
                        'fill_opacity': opacity
                    })

        # Earthquake decay circles
        earthquake_magnitudes_to_show = [7.0, 6.0, 5.0, 4.0]
        for mag in earthquake_magnitudes_to_show:
            if mag <= earthquake_magnitude:
                radius_km = calculate_earthquake_decay_radius(earthquake_magnitude, mag)
                if radius_km > 0:
                    all_circles.append({
                        'radius_km': radius_km,
                        'popup': f"Magnitude: {mag:.1f} Richter",
                        'tooltip': f"Magnitude: {mag:.1f} Richter",
                        'color': 'purple',
                        'fill_color': 'purple',
                        'fill_opacity': 0.2
                    })

        # Sort circles by radius in descending order (largest first)
        all_circles.sort(key=lambda c: c['radius_km'], reverse=True)

        # Draw the circles from largest to smallest
        for circle_data in all_circles:
            folium.Circle(
                location=[latitude, longitude],
                radius=circle_data['radius_km'] * 1000,
                popup=circle_data['popup'],
                tooltip=circle_data['tooltip'],
                color=circle_data['color'],
                fill=True,
                fillColor=circle_data['fill_color'],
                fillOpacity=circle_data['fill_opacity'],
                weight=2
            ).add_to(impact_map)
        
        # Add a main marker at the impact point on top of everything
        folium.Marker(
            location=[latitude, longitude],
            popup=f'<b>Impact Point</b><br>Lat: {latitude}<br>Lon: {longitude}',
            tooltip='Asteroid Impact Location',
            icon=folium.Icon(color='black', icon='warning-sign')
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
    
    avg_pop_density = 60
    estimated_affected = int(affected_area_km2 * avg_pop_density)
    
    return {
        "affected_area_km2": round(affected_area_km2, 2),
        "estimated_affected_population": estimated_affected,
        "note": "This is a rough estimate based on average global population density"
    }