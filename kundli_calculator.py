# kundli_calculator.py
from skyfield.api import load, Topos
from datetime import datetime
from utils import get_zodiac_sign, format_degree, get_house
from skyfield.api import utc

def calculate_planets(birth_date_str, birth_time_str, latitude, longitude):
    """
    Calculate planetary positions for given birth details.
    
    Args:
        birth_date_str: Birth date as string (YYYY/MM/DD)
        birth_time_str: Birth time as string (HH:MM)
        latitude: Geographic latitude
        longitude: Geographic longitude
    
    Returns:
        tuple: (planets_dict, ascendant_sign) where planets_dict contains
               planet positions with degree and house information
    """
    try:
        # Load ephemeris data
        ts = load.timescale()
        eph = load('de421.bsp')
        
        # Parse birth datetime
        birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", '%Y/%m/%d %H:%M')
        birth_dt = birth_dt.replace(tzinfo=utc)  # make it timezone aware
        
        # Create time object
        t = ts.utc(birth_dt.year, birth_dt.month, birth_dt.day, 
                   birth_dt.hour, birth_dt.minute)
        
        # Set observer location
        location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
        
        # Get Earth
        earth = eph['earth']
        
        # Calculate planetary positions
        planets_to_calc = {
            'Sun': eph['sun'],
            'Moon': eph['moon'],
            'Mercury': eph['mercury'],
            'Venus': eph['venus'],
            'Mars': eph['mars'],
            'Jupiter': eph['jupiter barycenter'],
            'Saturn': eph['saturn barycenter'],
        }
        
        planets = {}
        
        # Calculate ascendant (simplified calculation based on local sidereal time)
        # This is a rough calculation - actual ascendant calculation is more complex
        observer = earth + location
        lst_hours = t.gast  # Greenwich Apparent Sidereal Time
        # Adjust for longitude
        lst_deg = (lst_hours * 15 + longitude) % 360
        ascendant_degree = lst_deg % 360
        ascendant_sign = get_zodiac_sign(ascendant_degree)
        
        # Calculate planet positions
        for planet_name, planet_obj in planets_to_calc.items():
            # Get ecliptic longitude
            astrometric = observer.at(t).observe(planet_obj)
            lat, lon, distance = astrometric.ecliptic_latlon()
            degree = lon.degrees % 360
            
            planets[planet_name] = {
                'degree': format_degree(degree),
                'house': get_house(degree, ascendant_degree),
                'raw_degree': degree
            }
        
        return planets, f"{format_degree(ascendant_degree)} ({ascendant_sign})"
    
    except Exception as e:
        # Return error message
        return str(e), "Error"
