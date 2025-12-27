# forecast.py
from skyfield.api import load
from datetime import datetime
from utils import get_zodiac_sign
from skyfield.api import utc  # Import Skyfield's utc object

# Cache ephemeris and timescale at module load to avoid repeated IO
_TS = load.timescale()
_EPH = load('de421.bsp')

def daily_forecast():
    t = _TS.utc(datetime.now(tz=utc))  # Use timezone-aware datetime
    
    # Get Sun and Moon positions
    earth = _EPH['earth']
    sun = _EPH['sun']
    moon = _EPH['moon']
    
    sun_pos = earth.at(t).observe(sun).ecliptic_latlon()[1].degrees
    moon_pos = earth.at(t).observe(moon).ecliptic_latlon()[1].degrees
    
    return f"Today: Sun in {get_zodiac_sign(sun_pos)}, Moon in {get_zodiac_sign(moon_pos)}"