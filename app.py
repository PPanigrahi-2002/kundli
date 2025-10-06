# app.py
import streamlit as st
from kundli_calculator import calculate_planets
from kundali_chart import draw_kundali_chart
from forecasts import daily_forecast
from utils import format_date, format_planet_positions
from datetime import datetime

st.title("🪐 Kundli Generator AI")

# Inputs with validation
birth_date_str = st.text_input("Birth Date (YYYY/MM/DD)", "2000/01/01")
birth_time_str = st.text_input("Birth Time (HH:MM, 24-hour format)", "12:00")
latitude = st.number_input("Latitude", value=28.61, format="%.4f")
longitude = st.number_input("Longitude", value=77.21, format="%.4f")

# Validate inputs
try:
    birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", '%Y/%m/%d %H:%M')
    valid_input = True
except ValueError:
    st.error("Invalid date or time format. Use YYYY/MM/DD and HH:MM.")
    valid_input = False

if st.button("Generate Kundli") and valid_input:
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