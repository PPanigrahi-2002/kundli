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
4. Run the app: `streamlit run app.py`

## Features

- [ ] User input for birth details
- [ ] Calculation of planetary positions
- [ ] Display of Kundli chart

## Dependencies

- Streamlit
- Skyfield (for astronomical calculations)
