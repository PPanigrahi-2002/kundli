# utils.py
from datetime import datetime

def get_zodiac_sign(degree):
    """Map a degree (0-360) to its corresponding zodiac sign."""
    degree = degree % 360
    zodiac_signs = [
        ("Aries", 0, 30), ("Taurus", 30, 60), ("Gemini", 60, 90), ("Cancer", 90, 120),
        ("Leo", 120, 150), ("Virgo", 150, 180), ("Libra", 180, 210), ("Scorpio", 210, 240),
        ("Sagittarius", 240, 270), ("Capricorn", 270, 300), ("Aquarius", 300, 330), ("Pisces", 330, 360)
    ]
    for sign, start, end in zodiac_signs:
        if start <= degree < end:
            return sign
    return "Pisces"

def format_degree(degree):
    """Format a degree (0-360) as 'DD° Sign MM' (e.g., '15° Aries 30')."""
    degree = degree % 360
    sign = get_zodiac_sign(degree)
    degrees = int(degree % 30)
    minutes = int((degree % 1) * 60)
    return f"{degrees}° {sign} {minutes}'"

def get_house(degree, ascendant_degree=0):
    """Map a degree to an astrological house (equal house system)."""
    degree = (degree - ascendant_degree) % 360
    house = int(degree // 30) + 1
    return house if 1 <= house <= 12 else 12

def format_date(date_obj):
    """Format a datetime object into 'DD MMM YYYY'."""
    return date_obj.strftime("%d %b %Y")

def format_planets(planets_dict):
    """Return a formatted string of planets and their signs."""
    return "\n".join([f"{planet}: {sign}" for planet, sign in planets_dict.items()])

def format_planet_positions(planets_dict):
    """Return a formatted string of planets with degrees and houses."""
    return "\n".join([f"{planet}: {pos['degree']} (House {pos['house']})" for planet, pos in planets_dict.items()])