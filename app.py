# app.py
import streamlit as st
from kundli_calculator import calculate_planets
from kundali_chart import draw_kundali_chart
from forecasts import daily_forecast
from utils import format_date, format_planet_positions
from datetime import datetime, date
from geopy.geocoders import Nominatim
import ssl
import certifi
import time

st.title("🪐 Kundli Generator AI")

# Inputs with calendar and location
birth_date = st.date_input("Birth Date", value=date(2000, 1, 1))
birth_time_str = st.text_input("Birth Time (HH:MM, 24-hour format)", "12:00")

# Location search with suggestions
location_search = st.text_input("Type Birth Location (City, Country)", "")

# Get coordinates from location
latitude = None
longitude = None
valid_input = True
location_options = []

# Search for location suggestions when user types
if location_search and len(location_search) >= 3:
    try:
        ctx = ssl.create_default_context(cafile=certifi.where())
        geolocator = Nominatim(user_agent="kundli_generator", ssl_context=ctx)
        # Get multiple location results
        locations = geolocator.geocode(location_search, exactly_one=False, limit=5)
        
        if locations:
            # Create options from search results
            location_options = [loc.address for loc in locations]
            
            # Show dropdown with suggestions
            selected_location = st.selectbox(
                "Select Location from suggestions:",
                options=location_options,
                key="location_select"
            )
            
            # Get coordinates for selected location
            if selected_location:
                selected_loc_data = geolocator.geocode(selected_location)
                if selected_loc_data:
                    latitude = selected_loc_data.latitude
                    longitude = selected_loc_data.longitude
                    st.success(f"📍 Selected: {selected_location} (Lat: {latitude:.4f}, Lon: {longitude:.4f})")
        else:
            st.warning("No locations found. Try a different search term.")
            valid_input = False
            
    except Exception as e:
        st.error(f"Error searching location: {str(e)}")
        valid_input = False
elif location_search and len(location_search) < 3:
    st.info("Type at least 3 characters to search for locations")
    valid_input = False
else:
    st.info("Enter a location to begin (e.g., 'New Delhi', 'Mumbai', 'London')")
    valid_input = False

# Validate time input
try:
    birth_dt = datetime.combine(birth_date, datetime.strptime(birth_time_str, '%H:%M').time())
    birth_date_str = birth_date.strftime('%Y/%m/%d')
except ValueError:
    st.error("Invalid time format. Use HH:MM (24-hour format).")
    valid_input = False

if st.button("Generate Kundli") and valid_input and latitude and longitude:
    planets, ascendant = calculate_planets(birth_date_str, birth_time_str, latitude, longitude)

    if isinstance(planets, str):
        st.error(f"Error calculating Kundli: {planets}")
    else:
        st.subheader("🌟 Planet Positions & Predictions")
        st.text(format_planet_positions(planets))

        st.subheader("🪞 Ascendant (Lagna)")
        st.write(ascendant)

        st.subheader("📅 Birth Date")
        st.write(format_date(birth_dt))

        # Draw chart
        fig = draw_kundali_chart(planets, ascendant)
        st.pyplot(fig)

# Display daily forecast
st.subheader("🌙 Daily Forecast")
st.write(daily_forecast())
