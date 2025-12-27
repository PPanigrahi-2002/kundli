from skyfield.api import load, Topos
from datetime import datetime
from utils import get_zodiac_sign, format_degree, get_house
from skyfield.api import utc
from timezonefinder import TimezoneFinder
import pytz
import math
import numpy as np

# Cache ephemeris and timescale at module load to avoid repeated IO
_TS = load.timescale()
_EPH = load('de421.bsp')

def _ecliptic_lon_to_ra_dec(lambda_deg: float, obliquity_deg: float):
    """Convert ecliptic longitude at latitude 0 to equatorial RA/Dec in radians."""
    lam = math.radians(lambda_deg)
    eps = math.radians(obliquity_deg)
    sin_l = math.sin(lam)
    cos_l = math.cos(lam)
    cos_eps = math.cos(eps)
    sin_eps = math.sin(eps)
    y = sin_l * cos_eps
    x = cos_l
    ra = math.atan2(y, x)
    if ra < 0:
        ra += 2 * math.pi
    dec = math.asin(sin_l * sin_eps)
    return ra, dec

def _alt_az(ra: float, dec: float, lst_rad: float, lat_rad: float):
    """Compute altitude and azimuth (radians) from RA/Dec, LST, latitude."""
    H = (lst_rad - ra)
    H = (H + math.pi) % (2 * math.pi) - math.pi
    sin_alt = math.sin(lat_rad) * math.sin(dec) + math.cos(lat_rad) * math.cos(dec) * math.cos(H)
    alt = math.asin(max(-1.0, min(1.0, sin_alt)))
    y = math.sin(H)
    x = math.cos(H) * math.sin(lat_rad) - math.tan(dec) * math.cos(lat_rad)
    az = math.atan2(y, x)
    if az < 0:
        az += 2 * math.pi
    return alt, az, H

def compute_ascendant_degree(latitude: float, longitude: float, t) -> float:
    """Compute the ecliptic longitude of the Ascendant using analytic formula."""
    obliquity_deg = 23.439291
    eps = math.radians(obliquity_deg)
    lat_rad = math.radians(latitude)
    
    lst_hours = t.gast
    lst_deg = (lst_hours * 15.0 + longitude) % 360.0
    lst_rad = math.radians(lst_deg)
    
    # Analytic formula for Ascendant
    # tan(lambda) = -cos(RAMC) / (sin(RAMC)*cos(eps) + tan(lat)*sin(eps))
    # Using atan2(y, x) where y = -cos(RAMC), x = denom
    num = -math.cos(lst_rad)
    den = math.sin(lst_rad) * math.cos(eps) + math.tan(lat_rad) * math.sin(eps)
    asc_rad = math.atan2(num, den)
    asc_deg = math.degrees(asc_rad) % 360.0
    
    # Validation: The formula usually gives the Ascendant, but let's double check Azimuth
    # to ensure it's the Rising point (East), not Setting.
    ra, dec = _ecliptic_lon_to_ra_dec(asc_deg, obliquity_deg)
    alt, az, _ = _alt_az(ra, dec, lst_rad, lat_rad)
    az_deg = math.degrees(az) % 360.0
    
    # East is ~270. Range 200-340.
    # If Azimuth is West (~90), we found Descendant (or formula quadrant issue).
    if not (200 <= az_deg <= 340):
        # Flip 180 degrees
        asc_deg = (asc_deg + 180) % 360.0
        
    return asc_deg

def calculate_lunar_nodes(t, observer):
    """Approximate Rahu and Ketu positions using Moon and Sun data."""
    # Get Moon and Sun positions
    moon = observer.at(t).observe(_EPH['moon'])
    sun = observer.at(t).observe(_EPH['sun'])
    moon_lon, moon_lat, _ = moon.ecliptic_latlon()
    sun_lon, sun_lat, _ = sun.ecliptic_latlon()
    
    # Approximate lunar node longitude (simplified method)
    # In Vedic astrology, Rahu is near the ascending node, calculated more precisely with orbital elements
    # Here, we use a basic approximation based on mean node position (true nodes require nutation)
    # For simplicity, we'll use a placeholder; accurate calculation needs JPL ephemeris or interpolation
    # Using a rough estimate based on mean node motion (~19.3°/year retrograde)
    from skyfield.framelib import ecliptic_frame
    t0 = _TS.utc(2000, 1, 1)
    years_since = (t.utc_datetime() - t0.utc_datetime()).days / 365.25
    mean_node = 125.0 - 19.3 * years_since  # Approximate mean node longitude (J2000.0 starting point)
    mean_node = mean_node % 360.0
    rahu_degree = mean_node
    ketu_degree = (rahu_degree + 180.0) % 360.0
    
    return rahu_degree, ketu_degree

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
        # Parse the provided birth date and time
        birth_datetime_str = f"{birth_date_str} {birth_time_str}"
        birth_naive = datetime.strptime(birth_datetime_str, '%Y/%m/%d %H:%M')
        
        # Get timezone
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=latitude, lng=longitude) or 'Asia/Kolkata'
        local_tz = pytz.timezone(tz_name)
        birth_local = local_tz.localize(birth_naive)
        birth_dt = birth_local.astimezone(pytz.utc)
        
        t = _TS.utc(birth_dt.year, birth_dt.month, birth_dt.day, 
                   birth_dt.hour, birth_dt.minute)
        
        location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
        earth = _EPH['earth']
        observer = earth + location
        
        planets_to_calc = {
            'Sun': _EPH['sun'],
            'Moon': _EPH['moon'],
            'Mercury': _EPH['mercury'],
            'Venus': _EPH['venus'],
            'Mars': _EPH['mars'],
            'Jupiter': _EPH['jupiter barycenter'],
            'Saturn': _EPH['saturn barycenter'],
        }
        
        planets = {}
        
        # Calculate Lahiri Ayanamsa
        # J2000 epoch: 2000-01-01 12:00 TT
        # Lahiri Ayanamsa at J2000: ~23° 51' 11" = 23.853055 degrees
        # Precession rate: ~50.29 arcseconds/year
        # Formula: Ayanamsa = 23.853 + (YearsSince2000 * 50.29 / 3600)
        t0 = _TS.utc(2000, 1, 1, 12)
        days_since_j2000 = t.tt - t0.tt
        years_since_j2000 = days_since_j2000 / 365.25
        ayanamsa = 23.853055 + (years_since_j2000 * 50.29 / 3600.0)
        
        # Calculate Ascendant
        tropical_asc = compute_ascendant_degree(latitude, longitude, t)
        sidereal_asc = (tropical_asc - ayanamsa) % 360.0
        
        ascendant_degree = sidereal_asc
        ascendant_sign = get_zodiac_sign(ascendant_degree)
        
        # For Rashi Chart (Whole Sign Houses), we need sign indices (0-11)
        asc_sign_idx = int(ascendant_degree // 30)
        
        # Calculate positions for planets
        for planet_name, planet_obj in planets_to_calc.items():
            astrometric = observer.at(t).observe(planet_obj)
            lat, lon, distance = astrometric.ecliptic_latlon()
            
            # Convert to Sidereal
            tropical_deg = lon.degrees % 360
            sidereal_deg = (tropical_deg - ayanamsa) % 360.0
            degree = sidereal_deg
            
            # Rashi House Logic: (PlanetSign - AscSign) + 1
            planet_sign_idx = int(degree // 30)
            rashi_house = ((planet_sign_idx - asc_sign_idx) % 12) + 1
            
            planets[planet_name] = {
                'degree': format_degree(degree),
                'house': rashi_house,
                'raw_degree': degree
            }
        
        # Calculate lunar nodes (Rahu and Ketu)
        rahu_degree_tropical, ketu_degree_tropical = calculate_lunar_nodes(t, observer)
        
        # Convert to Sidereal
        rahu_degree = (rahu_degree_tropical - ayanamsa) % 360.0
        ketu_degree = (ketu_degree_tropical - ayanamsa) % 360.0
        
        rahu_sign_idx = int(rahu_degree // 30)
        rahu_house = ((rahu_sign_idx - asc_sign_idx) % 12) + 1
        
        planets['Rahu'] = {
            'degree': format_degree(rahu_degree),
            'house': rahu_house,
            'raw_degree': rahu_degree
        }
        
        ketu_sign_idx = int(ketu_degree // 30)
        ketu_house = ((ketu_sign_idx - asc_sign_idx) % 12) + 1
        
        planets['Ketu'] = {
            'degree': format_degree(ketu_degree),
            'house': ketu_house,
            'raw_degree': ketu_degree
        }
        
        return planets, f"{format_degree(ascendant_degree)} ({ascendant_sign})"
    
    except Exception as e:
        return str(e), "Error"

# Run with specific details for Binka, Sonepur, Odisha
latitude = 21.03  # Approximate latitude
longitude = 83.78  # Approximate longitude
planets, ascendant = calculate_planets("2002/10/01", "08:00", latitude, longitude)
print("Planets:", planets)
print("Ascendant:", ascendant)