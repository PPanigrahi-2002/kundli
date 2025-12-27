# Kundli MVP

A minimal viable product for generating Kundli (birth charts) using Python and Streamlit.

## Project Structure

- `app.py`: Main Streamlit app (user interface)
- `kundli_calculator.py`: Core logic for calculating planetary positions
- `utils.py`: Helper functions (degree → zodiac mapping, formatting, etc.)
- `requirements.txt`: List of dependencies (Streamlit, Skyfield, etc.)
- `data/`: Optional directory for storing ephemeris, CSVs, or JSON predictions
- `.venv/`: Virtual environment (ignore in version control)

## Setup

1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Ensure `de421.bsp` is present in the project root (already included)
5. To enable AI features, create a `.env` file with `GROQ_API_KEY=your_key`
6. Timezone is auto-detected from coordinates via TimezoneFinder for accurate ascendant.
7. Run the app: `streamlit run app.py`

## Features

- [x] User input for birth details
- [x] Calculation of planetary positions
- [x] Display of Kundli chart
- [x] AI insights and chat (requires `GROQ_API_KEY`)

## Dependencies

- Streamlit
- Skyfield (astronomical calculations)
- Geopy (location search)
- Matplotlib (chart)
- LangChain + Groq (AI features)
- TimezoneFinder + pytz (timezone accuracy)
