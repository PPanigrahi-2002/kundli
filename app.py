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

# Import AI features with error handling
try:
    from ai_chat import render_ai_features
    from ai_interpreter import create_ai_interpreter, DEPENDENCIES_AVAILABLE
    from config import Config
    AI_FEATURES_AVAILABLE = True
except ImportError as e:
    AI_FEATURES_AVAILABLE = False
    print(f"AI features not available: {e}")

# Initialize session state for AI interpreter (singleton pattern)
if "ai_interpreter" not in st.session_state:
    st.session_state.ai_interpreter = None
if "ai_initialized" not in st.session_state:
    st.session_state.ai_initialized = False

@st.cache_resource
def get_ai_interpreter():
    """Get AI interpreter instance (cached to avoid recreation)"""
    if AI_FEATURES_AVAILABLE:
        try:
            Config.validate_config()
            return create_ai_interpreter()
        except Exception as e:
            st.error(f"Failed to create AI interpreter: {str(e)}")
            return None
    return None

st.title("🪐 Kundli Generator AI")

# Create main tabs to separate basic Kundli from AI features
main_tab, ai_tab = st.tabs(["📊 Generate Kundli", "🤖 AI Features"])

# Sidebar for AI features
with st.sidebar:
    st.header("🤖 AI Features")
    
    # Check if AI features are available
    if not AI_FEATURES_AVAILABLE:
        st.warning("⚠️ AI Features Not Available")
        st.info("Install AI dependencies: pip install langchain langchain-groq python-dotenv groq")
    else:
        try:
            Config.validate_config()
            st.success("✅ AI Features Enabled")
            st.info("Generate your Kundli to unlock AI features!")
                
        except ValueError:
            st.warning("⚠️ AI Features Disabled")
            st.info("Set GROQ_API_KEY to enable AI features")
    
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("• AI-powered Kundli interpretation")
    st.markdown("• Conversational astrology chat")
    st.markdown("• Personalized insights")
    st.markdown("• Daily predictions")

# Main Kundli Generation Tab
with main_tab:
    st.subheader("📊 Generate Your Kundli")

    # Quick Presets (Speed Dial)
    st.markdown("**🚀 Quick Presets:**")
    if st.button("Load 'Vishesh'"):
        st.session_state.birth_date_input = date(2001, 6, 16)
        st.session_state.birth_time_input = "12:06"
        st.session_state.location_input = "Seoni, Madhya Pradesh"
        st.rerun()

    # Inputs with calendar and location
    # Use session state keys to allow programmatic updates
    if "birth_date_input" not in st.session_state:
        st.session_state.birth_date_input = date(2000, 1, 1)
    if "birth_time_input" not in st.session_state:
        st.session_state.birth_time_input = "12:00"
    if "location_input" not in st.session_state:
        st.session_state.location_input = ""

    birth_date = st.date_input("Birth Date", key="birth_date_input")
    birth_time_str = st.text_input("Birth Time (HH:MM, 24-hour format)", key="birth_time_input")

    # Location search with suggestions
    location_search = st.text_input("Type Birth Location (City, Country)", key="location_input")

    # Get coordinates from location
    latitude = None
    longitude = None
    valid_input = True
    location_options = []

    # Search for location suggestions when user types
    if location_search and len(location_search) >= 3:
        try:
            ctx = ssl.create_default_context(cafile=certifi.where())
            geolocator = Nominatim(
                user_agent="kundli_generator", 
                ssl_context=ctx,
                timeout=10  # Increase timeout
            )
            
            with st.spinner("Searching for locations..."):
                # Get multiple location results with retry
                locations = None
                for attempt in range(3):  # Try 3 times
                    try:
                        locations = geolocator.geocode(location_search, exactly_one=False, limit=5)
                        break
                    except Exception as retry_error:
                        if attempt == 2:  # Last attempt
                            raise retry_error
                        time.sleep(1)  # Wait 1 second before retry
            
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
                    try:
                        selected_loc_data = geolocator.geocode(selected_location, timeout=10)
                        if selected_loc_data:
                            latitude = selected_loc_data.latitude
                            longitude = selected_loc_data.longitude
                            st.success(f"📍 Selected: {selected_location} (Lat: {latitude:.4f}, Lon: {longitude:.4f})")
                    except Exception as coord_error:
                        st.warning(f"Could not get coordinates for selected location: {coord_error}")
                        valid_input = False
            else:
                st.warning("No locations found. Try a different search term.")
                valid_input = False
                
        except Exception as e:
            st.error(f"Error searching location: {str(e)}")
            st.info("💡 **Tip**: You can also manually enter coordinates if location search is not working.")
            
            # Manual coordinate input as fallback
            st.subheader("🔧 Manual Location Input")
            manual_lat = st.number_input("Enter Latitude:", value=0.0, format="%.4f", key="manual_lat")
            manual_lon = st.number_input("Enter Longitude:", value=0.0, format="%.4f", key="manual_lon")
            
            if manual_lat != 0.0 and manual_lon != 0.0:
                latitude = manual_lat
                longitude = manual_lon
                st.success(f"📍 Using manual coordinates: Lat {latitude:.4f}, Lon {longitude:.4f}")
                valid_input = True
    elif location_search and len(location_search) < 3:
        st.info("Type at least 3 characters to search for locations")
        valid_input = False
    else:
        st.info("Enter a location to begin (e.g., 'New Delhi', 'Mumbai', 'London')")
        
        # Quick reference for common Indian cities
        st.subheader("🏙️ Quick Reference - Major Indian Cities")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**North India:**")
            st.write("• New Delhi")
            st.write("• Mumbai")
            st.write("• Pune")
            st.write("• Jaipur")
        
        with col2:
            st.write("**South India:**")
            st.write("• Bangalore")
            st.write("• Chennai")
            st.write("• Hyderabad")
            st.write("• Kochi")
        
        with col3:
            st.write("**East/West:**")
            st.write("• Kolkata")
            st.write("• Ahmedabad")
            st.write("• Bhopal")
            st.write("• Indore")
        
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
            # Store birth chart data for AI features
            # Ensure selected_location is safely defined
            safe_location = (
                selected_location if 'selected_location' in locals() and selected_location else "Custom Coordinates"
            )

            birth_chart_data = {
                "planets": planets,
                "ascendant": ascendant,
                "birth_info": f"{format_date(birth_dt)} at {birth_time_str}, {safe_location}",
                "birth_dt": birth_dt
            }
            
            st.subheader("🌟 Planet Positions & Predictions")
            st.text(format_planet_positions(planets))

            st.subheader("🪞 Ascendant (Lagna)")
            st.write(ascendant)

            st.subheader("📅 Birth Date")
            st.write(format_date(birth_dt))

            # Draw chart
            fig = draw_kundali_chart(planets, ascendant)
            st.pyplot(fig)
            
            # Store birth chart data in session state for AI features
            st.session_state.birth_chart_data = birth_chart_data
            
            st.success("✅ Kundli generated successfully! Switch to the AI Features tab to get AI insights.")

    # Display daily forecast
    st.subheader("🌙 Daily Forecast")
    basic_forecast = daily_forecast()
    st.write(basic_forecast)

# AI Features Tab
with ai_tab:
    st.subheader("🤖 AI-Powered Astrology Features")
    
    # Check if birth chart data is available
    if "birth_chart_data" not in st.session_state:
        st.info("👆 Please generate your Kundli first in the 'Generate Kundli' tab to unlock AI features!")
    else:
        # Check if AI features are available
        if not AI_FEATURES_AVAILABLE:
            st.warning("AI features not available. Install dependencies: pip install langchain langchain-groq python-dotenv groq")
        else:
            try:
                Config.validate_config()
                st.success("✅ AI Features Ready!")
                
                # Show AI features
                render_ai_features(st.session_state.birth_chart_data)
                
            except ValueError as e:
                st.warning(f"AI features not available: {str(e)}")
                st.info("To enable AI features, please set your GROQ_API_KEY in environment variables or .env file")

