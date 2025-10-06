# kundli_chart.py
from utils import format_planet_positions

def draw_kundali_chart(planets, ascendant):
    """Return a Chart.js configuration for a Kundli chart and planet labels for tooltips."""
    # Map planets to their houses for visualization
    house_counts = {i: [] for i in range(1, 13)}
    for planet, pos in planets.items():
        house = pos['house']
        house_counts[house].append(planet)

    # Prepare data for Chart.js polar area chart
    labels = [f"House {i}" for i in range(1, 13)]
    data = [len(house_counts[i]) for i in range(1, 13)]  # Number of planets per house
    planet_labels = [", ".join(house_counts[i]) or "Empty" for i in range(1, 13)]

    chart_config = {
        "type": "polarArea",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Planets in Houses",
                "data": data,
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.6)", "rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)",
                    "rgba(75, 192, 192, 0.6)", "rgba(153, 102, 255, 0.6)", "rgba(255, 159, 64, 0.6)",
                    "rgba(199, 199, 199, 0.6)", "rgba(83, 102, 255, 0.6)", "rgba(255, 99, 71, 0.6)",
                    "rgba(144, 238, 144, 0.6)", "rgba(255, 105, 180, 0.6)", "rgba(128, 128, 128, 0.6)"
                ],
                "borderColor": ["#fff"] * 12,
                "borderWidth": 1
            }]
        },
        "options": {
            "plugins": {
                "title": {"display": True, "text": f"Kundli Chart (Ascendant: {ascendant})"},
                "tooltip": {}  # Empty tooltip config; logic moved to JavaScript
            },
            "scales": {
                "r": {
                    "angleLines": {"display": True},
                    "ticks": {"display": False}
                }
            }
        }
    }

    return chart_config, planet_labels, format_planet_positions(planets)