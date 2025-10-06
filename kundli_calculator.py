# kundli_chart.py
import matplotlib.pyplot as plt
from utils import format_planet_positions

def draw_kundali_chart(planets, ascendant):
    """Draw a North Indian style Kundli chart using Matplotlib."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    # Define house positions and labels (North Indian style)
    house_coords = [
        ((0.5, 1.0), "1st House"),  # Top center
        ((0.75, 0.75), "2nd House"),  # Top right
        ((1.0, 0.5), "3rd House"),  # Right center
        ((0.75, 0.25), "4th House"),  # Bottom right
        ((0.5, 0.0), "5th House"),  # Bottom center
        ((0.25, 0.25), "6th House"),  # Bottom left
        ((0.0, 0.5), "7th House"),  # Left center
        ((0.25, 0.75), "8th House"),  # Top left
        ((0.5, 0.5), "9th House"),  # Center right
        ((0.75, 0.5), "10th House"),  # Center
        ((0.5, 0.75), "11th House"),  # Center left
        ((0.25, 0.5), "12th House")  # Center bottom
    ]

    # Draw diamond shapes for houses
    for (x, y), label in house_coords:
        # Create diamond shape coordinates
        diamond = plt.Polygon([
            (x - 0.15, y), (x, y + 0.15), (x + 0.15, y), (x, y - 0.15)
        ], closed=True, fill=False, edgecolor='black')
        ax.add_patch(diamond)
        ax.text(x, y, label, ha='center', va='center', fontsize=10)

    # Draw diagonal lines to connect houses (traditional style)
    ax.plot([0.25, 0.75], [0.75, 0.25], 'k-')  # 8th to 4th
    ax.plot([0.75, 0.25], [0.75, 0.25], 'k-')  # 2nd to 6th
    ax.plot([0.25, 0.75], [0.25, 0.75], 'k-')  # 4th to 8th
    ax.plot([0.75, 0.25], [0.25, 0.75], 'k-')  # 6th to 2nd

    # Add ascendant marker (top of 1st house)
    ax.plot(0.5, 1.0, 'b^', markersize=10)  # Blue triangle for ascendant
    ax.text(0.5, 1.0, f'Ascendant: {ascendant}', ha='center', va='bottom', fontsize=10, weight='bold')

    # Map planets to their houses
    house_planets = {i: [] for i in range(1, 13)}
    for planet, pos in planets.items():
        house = pos['house']
        house_planets[house].append(f"{planet}: {pos['degree']}")

    # Add planet positions to respective houses
    for house_num, (coords, _) in enumerate(house_coords, 1):
        planets_in_house = house_planets[house_num]
        if planets_in_house:
            x, y = coords
            ax.text(x, y - 0.1, '\n'.join(planets_in_house), ha='center', va='top', fontsize=8)

    # Remove axes
    ax.axis('off')

    # Apply traditional Indian art style (simplified)
    ax.set_facecolor('#f4e4bc')  # Light golden background
    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig
