
from skyfield.api import load
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

def run():
    print("Loading simplified debug...")
    ts = load.timescale()
    t = ts.utc(2002, 10, 1, 6, 36) # 12:06 IST - 5:30 = 06:36 UTC
    
    # Check LST
    lon = 79.54
    gast = t.gast
    lst = (gast * 15 + lon) % 360
    print(f"GAST (hrs): {gast}")
    print(f"LST (deg): {lst}")

    # Sun RA check
    eph = load('de421.bsp')
    sun = eph['sun']
    earth = eph['earth']
    obs = earth
    ast = obs.at(t).observe(sun)
    ra, dec, _ = ast.radec()
    print(f"Sun RA (hrs): {ra.hours}")
    print(f"Sun RA (deg): {ra._degrees}")
    
    # Expected LST ~ Sun RA at Noon
    diff = lst - ra._degrees
    print(f"LST - SunRA: {diff} deg (Should be ~0 for Noon)")

if __name__ == "__main__":
    run()
