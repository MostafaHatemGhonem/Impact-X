import math

def calculate_mass_and_energy(actual_diameter_m, actual_velocity_ms):
    """
    Calculate the mass and kinetic energy of the asteroid.

    Args:
        actual_diameter_m (float): Diameter of the asteroid in meters.
        actual_velocity_ms (float): Velocity of the asteroid in m/s.

    Returns:
        dict: Dictionary containing mass, energy, and related values.
    """
    # Average density of a C-type asteroid (kg/m³)
    density = 2600  

    # Radius
    radius_m = actual_diameter_m / 2

    # Volume
    volume_m3 = (4 / 3) * math.pi * (radius_m ** 3)

    # Mass
    mass_kg = density * volume_m3

    # Kinetic energy (Joules)
    energy_joules = 0.5 * mass_kg * (actual_velocity_ms ** 2)

    return {
        "mass_kg": mass_kg,
        "energy_joules": energy_joules,
        "density_kg_m3": density,
        "radius_m": radius_m,
        "volume_m3": volume_m3
    }


def calculate_impact_effects(kinetic_energy_joules, impact_density, is_ocean=False):
    """
    Calculate asteroid impact effects.

    Args:
        kinetic_energy_joules (float): Impact energy in joules.
        impact_density (float): Density of impact site (kg/m³).
        is_ocean (bool): True if the impact is in an ocean.

    Returns:
        dict: Dictionary containing crater size, depth, earthquake magnitude, etc.
    """
    g = 9.81  # gravity (m/s²)

    # Convert energy to megatons TNT
    megatons_tnt = kinetic_energy_joules / 4.184e15

    # Crater diameter (km) using simplified empirical formula
    crater_diameter_km = 1.161 * ((kinetic_energy_joules / 1e15) ** 0.294)

    # Crater depth (km)
    crater_depth_km = 0.2 * crater_diameter_km

    # Tsunami height if impact occurs in the ocean
    tsunami_height_m = None
    if is_ocean:
        ocean_depth_m = 4000
        tsunami_height_m = 0.8 * math.sqrt(kinetic_energy_joules) / (ocean_depth_m ** 0.75)

    # Earthquake magnitude (Richter scale approximation)
    earthquake_magnitude = 0.67 * math.log10(kinetic_energy_joules) - 5.87

    return {
        "megatons_tnt": megatons_tnt,
        "crater_diameter_km": crater_diameter_km,
        "crater_depth_km": crater_depth_km,
        "earthquake_magnitude": earthquake_magnitude,
        "tsunami_height_m": tsunami_height_m,
        "is_ocean_impact": is_ocean
    }


def estimate_diameter_from_magnitude(h_magnitude, albedo=0.15):
    """
    Estimate asteroid diameter from its absolute magnitude (H).

    Args:
        h_magnitude (float): Absolute magnitude of the asteroid.
        albedo (float): Reflectivity of the asteroid.

    Returns:
        float: Estimated diameter in kilometers.
    """
    return 1329 / math.sqrt(albedo) * math.pow(10, -0.2 * h_magnitude)


def calculate_risk_assessment(energy_megatons, min_distance_au):
    """
    Estimate risk level based on energy and minimum distance.
    """
    risk_score = energy_megatons / (min_distance_au * 100)
    if risk_score > 1000:
        risk_level = "High"
    elif risk_score > 100:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }


def calculate_damage_radii(energy_megatons):
    """
    Approximate destruction radii (km) based on energy in megatons.
    """
    if energy_megatons <= 0:
        return {
            "severe_damage_km": None,
            "moderate_damage_km": None,
            "light_damage_km": None
        }

    # Approximation based on NASA / Earth Impact Effects Program
    total_destruction = 0.042 * (energy_megatons ** (1 / 3))
    severe_damage = 0.084 * (energy_megatons ** (1 / 3))
    moderate_damage = 0.17 * (energy_megatons ** (1 / 3))
    window_breakage = 0.34 * (energy_megatons ** (1 / 3))

    return {
        "total_destruction_km": total_destruction,
        "severe_damage_km": severe_damage,
        "moderate_damage_km": moderate_damage,
        "window_breakage_km": window_breakage,
        "light_damage_km": window_breakage  # alias
    }
def full_impact_calculation(diameter_m, velocity_ms, is_ocean=False, impact_density=2700):
    """
    Perform full asteroid impact calculations.
    """
    # Mass and energy
    mass_energy = calculate_mass_and_energy(diameter_m, velocity_ms)

    # Impact effects
    impact_effects = calculate_impact_effects(
        mass_energy["energy_joules"],
        impact_density,
        is_ocean
    )

    # Damage radii
    damage_radii = calculate_damage_radii(impact_effects["megatons_tnt"])

    # Combine results
    results = {
        **mass_energy,
        **impact_effects,
        "damage_radii_km": damage_radii
    }

    return results