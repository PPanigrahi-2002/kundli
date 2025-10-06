# kundali_chart.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_kundali_chart(planets, ascendant):
    """Draw a North Indian style Kundli chart using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    
    # Draw the main diamond shape (outer border)
    outer_diamond = patches.Polygon([
        (0.5, 1.0),   # top
        (1.0, 0.5),   # right
        (0.5, 0.0),   # bottom
        (0.0, 0.5)    # left
    ], fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(outer_diamond)
    
    # Draw inner cross to divide into houses
    ax.plot([0.5, 0.5], [0.0, 1.0], 'k-', linewidth=1.5)  # vertical line
    ax.plot([0.0, 1.0], [0.5, 0.5], 'k-', linewidth=1.5)  # horizontal line
    ax.plot([0.0, 1.0], [1.0, 0.0], 'k-', linewidth=1.5)  # diagonal top-left to bottom-right
    ax.plot([0.0, 1.0], [0.0, 1.0], 'k-', linewidth=1.5)  # diagonal bottom-left to top-right
    
    # Define house positions (North Indian style - 12 triangular sections)
    # Position format: (x, y, house_number)
    house_positions = [
        (0.5, 0.85, 1),    # 1st house - top center
        (0.7, 0.7, 2),     # 2nd house - top right diagonal
        (0.85, 0.5, 3),    # 3rd house - right center
        (0.7, 0.3, 4),     # 4th house - bottom right diagonal
        (0.5, 0.15, 5),    # 5th house - bottom center
        (0.3, 0.3, 6),     # 6th house - bottom left diagonal
        (0.15, 0.5, 7),    # 7th house - left center
        (0.3, 0.7, 8),     # 8th house - top left diagonal
        (0.35, 0.55, 9),   # 9th house - inner left
        (0.5, 0.6, 10),    # 10th house - inner top
        (0.65, 0.55, 11),  # 11th house - inner right
        (0.5, 0.4, 12)     # 12th house - inner bottom
    ]
    
    # Group planets by house
    house_planets = {i: [] for i in range(1, 13)}
    for planet, pos in planets.items():
        house = pos['house']
        house_planets[house].append(f"{planet[:3]}")  # abbreviate planet names
    
    # Draw house numbers and planets
    for x, y, house_num in house_positions:
        # Draw house number
        ax.text(x, y + 0.05, f"H{house_num}", ha='center', va='center', 
                fontsize=10, weight='bold', color='navy')
        
        # Draw planets in this house
        if house_planets[house_num]:
            planet_text = '\n'.join(house_planets[house_num])
            ax.text(x, y - 0.05, planet_text, ha='center', va='center', 
                    fontsize=11, color='darkred', weight='bold')
    
    # Add ascendant marker at 1st house
    ax.text(0.5, 0.95, f"ASC: {ascendant}", ha='center', va='center', 
            fontsize=10, weight='bold', color='green', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='green'))
    
    # Set limits and remove axes
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.axis('off')
    
    # Set background color (traditional parchment look)
    fig.patch.set_facecolor('#f5f5dc')  # beige
    ax.set_facecolor('#fffef0')  # light cream
    
    # Add title
    ax.text(0.5, 1.05, "Kundli Chart (North Indian Style)", 
            ha='center', va='bottom', fontsize=14, weight='bold')
    
    plt.tight_layout()
    
    return fig
