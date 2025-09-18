
# Artistic tide-like animation: volume, color, speed, height represent different indicators
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 8))

# Load data
df = pd.read_csv('water_potability.csv')
df = df.dropna()



# Particle/point cloud art animation for water quality indicators
indicators = [col for col in df.columns if col != 'Potability']
num_ind = len(indicators)
num_points = len(df)
colors = plt.cm.rainbow(np.linspace(0, 1, num_ind))

 # Normalization function
def norm(arr):
    arr = np.array(arr)
    return (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)

 # Point attributes: position, color, size, speed
point_x = np.random.uniform(0, 1, (num_ind, num_points)) * 12 - 6  # Random initial position
point_y = np.random.uniform(0, 1, (num_ind, num_points)) * 6 - 3
sizes = [norm(df[ind]) * 80 + 20 for ind in indicators]
speeds = [norm(df[ind]) * 0.08 + 0.02 for ind in indicators]
color_vals = [norm(df[ind]) for ind in indicators]

scatters = []
for i in range(num_ind):
    scatter = ax.scatter(point_x[i], point_y[i], s=sizes[i], c=colors[i], alpha=0.7, label=indicators[i])
    scatters.append(scatter)

ax.set_xlim(-6, 6)
ax.set_ylim(-3, 3)
ax.set_title('Artistic Water Quality: Particle Flow', fontsize=24, color='white', fontweight='bold', pad=20)
ax.set_xlabel('X', fontsize=16, color='white')
ax.set_ylabel('Y', fontsize=16, color='white')
ax.legend(loc='upper right', fontsize=12, frameon=False)
ax.set_facecolor('#222244')
fig.patch.set_facecolor('#222244')
for spine in ax.spines.values():
    spine.set_edgecolor('white')
    spine.set_linewidth(2)
plt.grid(False)
plt.tight_layout()

def init():
    for i, scatter in enumerate(scatters):
        scatter.set_offsets(np.c_[point_x[i], point_y[i]])
    return scatters

def animate(frame):
    for i in range(num_ind):
    # Make points drift along circular trajectories, with speed and radius controlled by data
        angle = frame * speeds[i] + np.linspace(0, 2*np.pi, num_points)
        radius = norm(df[indicators[i]]) * 2 + 1
        cx = np.cos(angle) * radius
        cy = np.sin(angle) * radius
    # Make points slowly drift on the canvas
        point_x[i] = cx + np.sin(frame * 0.01 + i) * 2
        point_y[i] = cy + np.cos(frame * 0.01 + i) * 1.2
        scatters[i].set_offsets(np.c_[point_x[i], point_y[i]])
    # Color gradient
        scatters[i].set_color(colors[i])
        scatters[i].set_sizes(sizes[i])
    return scatters

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=600, interval=60, blit=True, repeat=True)
plt.show()
