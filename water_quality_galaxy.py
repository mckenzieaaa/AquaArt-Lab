# Water Quality Galaxy Art Visualization
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.patches import Circle
import random

# Set dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(16, 10))

# Load data
df = pd.read_csv('water_potability.csv')
df = df.dropna()

print(f"Data loaded successfully, {len(df)} records found")

# Water quality indicators
indicators = [col for col in df.columns if col != 'Potability']
num_samples = len(df)

# Normalization function
def normalize_data(data):
    """Normalize data to 0-1 range"""
    data = np.array(data)
    return (data - data.min()) / (data.max() - data.min() + 1e-8)

# Create galaxy spiral arms effect
def create_galaxy_arms(num_arms=3, points_per_arm=None):
    """Create galaxy spiral arm coordinates"""
    if points_per_arm is None:
        points_per_arm = num_samples // num_arms
    
    galaxy_x = []
    galaxy_y = []
    arm_ids = []
    
    for arm in range(num_arms):
        # Parameters for each spiral arm
        arm_offset = arm * 2 * np.pi / num_arms
        
        # Spiral parameters
        t = np.linspace(0, 4 * np.pi, points_per_arm)
        r = 0.5 + 2 * t / (4 * np.pi)  # Radius increases with angle
        
        # Spiral coordinates
        x = r * np.cos(t + arm_offset)
        y = r * np.sin(t + arm_offset)
        
        # Add random noise for more natural appearance
        noise_scale = 0.3
        x += np.random.normal(0, noise_scale, len(x))
        y += np.random.normal(0, noise_scale, len(y))
        
        galaxy_x.extend(x)
        galaxy_y.extend(y)
        arm_ids.extend([arm] * points_per_arm)
    
    return np.array(galaxy_x), np.array(galaxy_y), np.array(arm_ids)

# Generate galaxy coordinates
galaxy_x, galaxy_y, arm_ids = create_galaxy_arms(num_arms=len(indicators))

# Assign colors and attributes for each water quality indicator
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE']
indicator_colors = colors[:len(indicators)]

# Set point attributes based on water quality data
point_sizes = []
point_alphas = []
point_colors_mapped = []

for i, indicator in enumerate(indicators):
    # Normalize current indicator data
    normalized_values = normalize_data(df[indicator])
    
    # Point size: larger values = larger points
    sizes = normalized_values * 60 + 10
    point_sizes.extend(sizes[:len(galaxy_x)//len(indicators)])
    
    # Transparency: larger values = brighter
    alphas = normalized_values * 0.8 + 0.2
    point_alphas.extend(alphas[:len(galaxy_x)//len(indicators)])
    
    # Color mapping
    colors_for_indicator = [indicator_colors[i]] * (len(galaxy_x)//len(indicators))
    point_colors_mapped.extend(colors_for_indicator)

# Create scatter plot
scatter = ax.scatter(galaxy_x, galaxy_y, 
                    s=point_sizes, 
                    c=point_colors_mapped, 
                    alpha=0.7, 
                    edgecolors='white', 
                    linewidths=0.5)

# Add central black hole effect
center_circle = Circle((0, 0), 0.3, color='black', alpha=0.9)
ax.add_patch(center_circle)
center_glow = Circle((0, 0), 0.5, color='white', alpha=0.1)
ax.add_patch(center_glow)

# Set figure style
ax.set_xlim(-8, 8)
ax.set_ylim(-6, 6)
ax.set_title('Water Quality Galaxy Visualization', 
             fontsize=28, color='white', fontweight='bold', pad=30)
ax.set_xlabel('Galaxy X Coordinate', fontsize=16, color='white')
ax.set_ylabel('Galaxy Y Coordinate', fontsize=16, color='white')

# Set background
ax.set_facecolor('#0a0a1a')
fig.patch.set_facecolor('#0a0a1a')

# Remove axis ticks but keep labels
ax.set_xticks([])
ax.set_yticks([])

# Remove borders
for spine in ax.spines.values():
    spine.set_visible(False)

# Add legend
legend_elements = []
for i, indicator in enumerate(indicators):
    legend_elements.append(plt.scatter([], [], c=indicator_colors[i], 
                                     s=100, label=indicator, 
                                     edgecolors='white', linewidths=0.5))

ax.legend(handles=legend_elements, loc='upper left', 
          fontsize=12, frameon=False, labelcolor='white')

# Add starry background
np.random.seed(42)
star_x = np.random.uniform(-8, 8, 200)
star_y = np.random.uniform(-6, 6, 200)
star_sizes = np.random.uniform(1, 5, 200)
ax.scatter(star_x, star_y, s=star_sizes, c='white', alpha=0.3, marker='*')

# Animation function
rotation_angle = 0

def animate(frame):
    global rotation_angle, scatter
    
    # Rotation angle
    rotation_angle += 0.02
    
    # Rotate coordinates
    cos_angle = np.cos(rotation_angle)
    sin_angle = np.sin(rotation_angle)
    
    # Apply rotation matrix
    rotated_x = galaxy_x * cos_angle - galaxy_y * sin_angle
    rotated_y = galaxy_x * sin_angle + galaxy_y * cos_angle
    
    # Update scatter plot positions
    scatter.set_offsets(np.column_stack((rotated_x, rotated_y)))
    
    # Add breathing effect (size changes)
    breathing_effect = 1 + 0.1 * np.sin(frame * 0.1)
    new_sizes = np.array(point_sizes) * breathing_effect
    scatter.set_sizes(new_sizes)
    
    return scatter,

# Create animation
print("Starting galaxy animation...")
ani = animation.FuncAnimation(fig, animate, frames=200, interval=100, 
                            blit=False, repeat=True)

plt.tight_layout()
plt.show()

print("Water Quality Galaxy visualization complete!")