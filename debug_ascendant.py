
from skyfield.api import load, Topos
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import math
import numpy as np

def _ecliptic_lon_to_ra_dec(lambda_deg: float, obliquity_deg: float):
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

def debug_run():
    # User Case: 2002/10/01 12:06 (Noon)
    # Location: Seoni, MP (22.08, 79.54 approx)
    date_str = "2002/10/01"
    time_str = "12:06"
    lat = 22.0869
    lon = 79.5435
    
    print(f"Debugging for {date_str} {time_str} at {lat}, {lon}")
    
    ts = load.timescale()
    eph = load('de421.bsp')
    
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    print(f"Timezone: {tz_name}")
    
    local = pytz.timezone(tz_name).localize(naive)
    utc_dt = local.astimezone(pytz.utc)
    
    t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute)
    
    # Calculate Sun Position
    sun = eph['sun']
    earth = eph['earth']
    obs = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    astrometric = obs.at(t).observe(sun)
    _, sun_lon, _ = astrometric.ecliptic_latlon()
    sun_deg = sun_lon.degrees % 360
    print(f"Sun Longitude: {sun_deg} (Western Tropical)")
    
    # Calculate Ascendant
    obliquity = 23.439291
    lst_hours = t.gast
    lst_deg = (lst_hours * 15.0 + lon) % 360.0
    lst_rad = math.radians(lst_deg)
    lat_rad = math.radians(lat)
    
    print(f"LST (deg): {lst_deg}")
    
    lambdas = np.linspace(0.0, 360.0, 361)
    print("\nScanning Ecliptic intersections with Horizon:")
    for lam in lambdas[::10]: # Check every 10 deg
        ra, dec = _ecliptic_lon_to_ra_dec(lam, obliquity)
        alt, az, _ = _alt_az(ra, dec, lst_rad, lat_rad)
        # Check if near horizon (alt ~ 0)
        if abs(alt) < 0.1:
            print(f"Lambda {lam:.1f}: Alt {math.degrees(alt):.1f}, Az {math.degrees(az):.1f}")

if __name__ == "__main__":
    debug_run()
