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
        (0.5, 0.72, 1),    # 1st house - Top (Lagna)
        (0.25, 0.88, 2),   # 2nd house - Top Left - Calculator Centroid
        (0.12, 0.75, 3),   # 3rd house - Left Upper - Calculator Centroid
        (0.25, 0.50, 4),   # 4th house - Left Center (Sukh)
        (0.12, 0.25, 5),   # 5th house - Left Lower - Calculator Centroid
        (0.25, 0.12, 6),   # 6th house - Bottom Left - Calculator Centroid
        (0.5, 0.28, 7),    # 7th house - Bottom (Kalatra)
        (0.75, 0.12, 8),   # 8th house - Bottom Right - Calculator Centroid
        (0.88, 0.25, 9),   # 9th house - Right Lower - Calculator Centroid
        (0.75, 0.50, 10),  # 10th house - Right Center (Karma)
        (0.88, 0.75, 11),  # 11th house - Right Upper - Calculator Centroid
        (0.75, 0.88, 12)   # 12th house - Top Right - Calculator Centroid
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

    # Vedic Planet Names
    planet_names = {
        'Sun': 'Surya', 'Moon': 'Chandra', 'Mars': 'Mangal',
        'Mercury': 'Budh', 'Jupiter': 'Guru', 'Venus': 'Shukra',
        'Saturn': 'Shani', 'Rahu': 'Rahu', 'Ketu': 'Ketu'
    }
    
    # Group planets by house
    house_planets = {i: [] for i in range(1, 13)}
    for planet, pos in planets.items():
        house = pos['house']
        label = planet_names.get(planet, planet)
        house_planets[house].append(label)
    
    # Define Sign/House Number positions (Outer edges of the triangles)
    # Fixed to ensure they are NOT on the diagonals
    sign_positions = [
        (0.5, 0.94, 1),    # H1 Top Center
        (0.30, 0.88, 2),   # H2 Top Left (Upper)
        (0.10, 0.70, 3),   # H3 Top Left (Lower)
        (0.18, 0.5, 4),    # H4 Left Center
        (0.10, 0.30, 5),   # H5 Bottom Left (Upper)
        (0.30, 0.12, 6),   # H6 Bottom Left (Lower)
        (0.5, 0.06, 7),    # H7 Bottom Center
        (0.70, 0.12, 8),   # H8 Bottom Right (Lower)
        (0.90, 0.30, 9),   # H9 Bottom Right (Upper)
        (0.82, 0.5, 10),   # H10 Right Center
        (0.90, 0.70, 11),  # H11 Top Right (Lower)
        (0.70, 0.88, 12)   # H12 Top Right (Upper)
    ]

    # Draw Sign Numbers (Rashi Numbers) at outer positions
    # Standard North Indian charts show the Rashi number (1=Aries, 5=Leo) in the house
    for x, y, house_num in sign_positions:
        # Calculate Rashi number (1-12)
        sign_idx = (asc_idx + house_num - 1) % 12
        sign_number = sign_idx + 1
        
        ax.text(x, y, f"{sign_number}", ha='center', va='center', 
                fontsize=10, color='white', weight='bold')

    # Draw Planets and Special Labels (Lagna) at Center positions
    for x, y, house_num in house_positions:
        # Get planets for this house
        planets_list = house_planets.get(house_num, [])
        
        # Special handling for H1 (Lagna)
        if house_num == 1:
            if not planets_list:
                # If transparent, just show Lagna
                ax.text(x, y, "Lagna", ha='center', va='center', fontsize=10, color='#FFD700', weight='bold') # Gold
            else:
                # Show Lagna, then planets below
                text_content = "Lagna\n" + '\n'.join(planets_list)
                ax.text(x, y, text_content, ha='center', va='center', fontsize=9, color='#FFD700', weight='bold')
        else:
            if planets_list:
                # Stack planets
                text_content = '\n'.join(planets_list)
                ax.text(x, y, text_content, ha='center', va='center', fontsize=9, color='#FFD700', weight='bold')
    
    # Set limits and remove axes
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    
    plt.tight_layout()
    return fig
