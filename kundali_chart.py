# kundali_chart.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import get_zodiac_sign

def draw_kundali_chart(planets, ascendant):
    """Draw a North Indian style Kundli chart using Matplotlib."""
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')
    
    # Set dark brown background like the reference image
    fig.patch.set_facecolor('#8B4513')  # dark brown
    ax.set_facecolor('#8B4513')  # dark brown
    
    # Draw standard North Indian Chart (Square with Diagonals and Diamond)
    
    # 1. Outer Box (Square)
    outer_box = patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor='white', linewidth=2)
    ax.add_patch(outer_box)
    
    # 2. Diagonals (X shape)
    ax.plot([0, 1], [0, 1], 'w-', linewidth=1.5)
    ax.plot([0, 1], [1, 0], 'w-', linewidth=1.5)
    
    # 3. Inner Diamond (connecting midpoints)
    inner_diamond = patches.Polygon([
        (0.5, 1.0),   # top
        (1.0, 0.5),   # right
        (0.5, 0.0),   # bottom
        (0.0, 0.5)    # left
    ], fill=False, edgecolor='white', linewidth=1.5)
    ax.add_patch(inner_diamond)
    
    # Define house positions (North Indian style - 12 triangular sections)
    # Position format: (x, y, house_number)
    # Following the exact layout from the reference image
    house_positions = [
        (0.5, 0.82, 1),    # 1st house - Top (Lagna) - Lowered slightly
        (0.22, 0.80, 2),   # 2nd house - Top Left - Moved Left
        (0.12, 0.60, 3),   # 3rd house - Left Upper - Moved Left
        (0.35, 0.5, 4),    # 4th house - Left Center (Sukh)
        (0.12, 0.40, 5),   # 5th house - Left Lower - Moved Left
        (0.22, 0.20, 6),   # 6th house - Bottom Left - Moved Left
        (0.5, 0.15, 7),    # 7th house - Bottom (Kalatra)
        (0.78, 0.20, 8),   # 8th house - Bottom Right - Moved Right
        (0.88, 0.40, 9),   # 9th house - Right Lower - Moved Right
        (0.65, 0.5, 10),   # 10th house - Right Center (Karma)
        (0.88, 0.60, 11),  # 11th house - Right Upper - Moved Right
        (0.78, 0.80, 12)   # 12th house - Top Right - Moved Right
    ]
    
    # Helper: zodiac sequence and ascendant sign extraction
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    def extract_asc_sign(asc_text):
        # asc_text example: "15° Aries 30' (Aries)" or "15° Aries 30'"
        if '(' in asc_text and ')' in asc_text:
            return asc_text.split('(')[-1].split(')')[0].strip()
        # Fallback: use get_zodiac_sign from raw degree if available in planets context (not here)
        # Try to find any known sign token in the asc_text
        for sign in zodiac_signs:
            if sign in asc_text:
                return sign
        return "Aries"

    asc_sign = extract_asc_sign(ascendant)
    try:
        asc_idx = zodiac_signs.index(asc_sign)
    except ValueError:
        asc_idx = 0

    # Short planet names for better visualization
    short_names = {
        'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma',
        'Mercury': 'Me', 'Jupiter': 'Ju', 'Venus': 'Ve',
        'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke'
    }
    
    # Group planets by house
    house_planets = {i: [] for i in range(1, 13)}
    for planet, pos in planets.items():
        house = pos['house']
        label = short_names.get(planet, planet[:2])
        house_planets[house].append(label)
    
    # Combine planets in the same house like in reference image
    house_planets_combined = {}
    for house_num, planets_list in house_planets.items():
        if planets_list:
            # Join planets with space like "Budh Mer^ Mangal"
            house_planets_combined[house_num] = ' '.join(planets_list)
        else:
            house_planets_combined[house_num] = ""
    
    # Draw house numbers, sign labels, and planets
    for x, y, house_num in house_positions:
        # Compute sign for this house starting from ascendant
        sign_label = zodiac_signs[(asc_idx + house_num - 1) % 12]
        
        # Draw house number and sign in the format shown in reference chart
        ax.text(x, y + 0.08, f"{house_num} {sign_label[:3]}", ha='center', va='center', 
                fontsize=10, weight='bold', color='white')
        
        # Get planets for this house
        planets_list = house_planets.get(house_num, [])

        if planets_list:
            # Chunk planets (max 2 per line) to prevent wide text overlap
            chunks = [planets_list[i:i+2] for i in range(0, len(planets_list), 2)]
            house_planets_text = '\n'.join([' '.join(chunk) for chunk in chunks])
            
            # Reduce font size slightly and use multiline
            ax.text(x, y - 0.04, house_planets_text, ha='center', va='center', 
                    fontsize=8, color='yellow', weight='bold')
    
    # Remove the ascendant marker box as it's not in the reference chart
    # The ascendant info is already shown in the 1st house
    
    # Set limits and remove axes
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    
    # No title needed as it matches the mobile app style
    
    plt.tight_layout()
    
    return fig
