# Enhanced Interactive Water Quality Art Visualization
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import Circle
import matplotlib.patches as patches

class EnhancedWaterArtVisualization:
    def __init__(self):
        plt.style.use('dark_background')
        
        # Create figure with 16:9 aspect ratio (1920x1080 optimized)
        self.fig = plt.figure(figsize=(19.2, 10.8))
        
        # Main visualization area
        self.ax_main = plt.subplot2grid((4, 6), (0, 1), colspan=4, rowspan=3)
        
        # Data statistics panel (right side)
        self.ax_stats = plt.subplot2grid((4, 6), (0, 5), colspan=1, rowspan=2)
        
        # Data distribution panel (bottom right)
        self.ax_dist = plt.subplot2grid((4, 6), (2, 5), colspan=1, rowspan=1)
        
        # Load data
        self.df = pd.read_csv('water_potability.csv')
        self.df = self.df.dropna()
        
        # Water quality indicators
        self.indicators = [col for col in self.df.columns if col != 'Potability']
        self.current_indicator = self.indicators[0]
        self.current_mode = 'galaxy'
        
        # Color scheme with better contrast
        self.indicator_colors = {
            'ph': '#FF6B6B',              # Red
            'Hardness': '#4ECDC4',        # Cyan  
            'Solids': '#45B7D1',          # Blue
            'Chloramines': '#96CEB4',     # Green
            'Sulfate': '#FFD93D',         # Bright Yellow
            'Conductivity': '#A8E6CF',    # Light Green
            'Organic_carbon': '#FF8B94',  # Pink
            'Trihalomethanes': '#B4A7D6', # Lavender
            'Turbidity': '#D4A574'        # Orange
        }
        
        # Animation control
        self.ani = None
        self.frame = 0
        
        # Create control panel
        self.create_control_panel()
        
        # Initialize visualization
        self.update_visualization()
        
        print("Enhanced Interactive Water Quality Art Visualization started!")
        print("Left: Switch indicators | Right: Switch art modes | Data stats shown on right panel")
    
    def normalize(self, data):
        """Data normalization to 0-1 range"""
        data = np.array(data)
        return (data - data.min()) / (data.max() - data.min() + 1e-8)
    
    def create_control_panel(self):
        """Create enhanced control buttons with better layout"""
        self.buttons = {}
        
        # Water quality indicator buttons (left side)
        button_height = 0.07
        button_width = 0.12
        start_y = 0.85
        
        for i, indicator in enumerate(self.indicators):
            y_pos = start_y - i * (button_height + 0.015)
            ax_button = self.fig.add_axes([0.02, y_pos, button_width, button_height])
            
            # Button styling with better visibility
            color = self.indicator_colors.get(indicator, '#888888')
            if indicator == self.current_indicator:
                color = '#FFFFFF'
                text_color = 'black'
            else:
                text_color = 'white'
            
            button = Button(ax_button, indicator, color=color, hovercolor='lightgray')
            button.label.set_color(text_color)
            button.label.set_fontweight('bold')
            button.on_clicked(lambda x, ind=indicator: self.change_indicator(ind))
            self.buttons[indicator] = button
        
        # Art mode buttons (bottom)
        modes = [
            ('🌌 Galaxy', 'galaxy'),
            ('✨ Particle', 'particle'), 
            ('🌊 Wave', 'wave'),
            ('⚡ Energy Field', 'energy')
        ]
        
        mode_y = 0.02
        mode_width = 0.15
        
        for i, (name, mode) in enumerate(modes):
            x_pos = 0.2 + i * (mode_width + 0.02)
            ax_button = self.fig.add_axes([x_pos, mode_y, mode_width, 0.06])
            
            color = '#FFD700' if mode == self.current_mode else '#444444'
            button = Button(ax_button, name, color=color, hovercolor='lightgray')
            button.label.set_fontweight('bold')
            button.on_clicked(lambda x, m=mode: self.change_mode(m))
            self.buttons[f'mode_{mode}'] = button
    
    def update_data_panels(self):
        """Update data statistics and distribution panels"""
        current_data = self.df[self.current_indicator]
        
        # Clear previous content
        self.ax_stats.clear()
        self.ax_dist.clear()
        
        # Statistics panel
        self.ax_stats.set_facecolor('#1a1a2e')
        self.ax_stats.set_title(f'{self.current_indicator}\nStatistics', 
                               fontsize=12, color='white', fontweight='bold')
        
        # Calculate statistics
        stats = {
            'Count': len(current_data),
            'Mean': f'{current_data.mean():.2f}',
            'Median': f'{current_data.median():.2f}',
            'Std': f'{current_data.std():.2f}',
            'Min': f'{current_data.min():.2f}',
            'Max': f'{current_data.max():.2f}',
            'Range': f'{current_data.max() - current_data.min():.2f}'
        }
        
        # Display statistics as text
        y_pos = 0.9
        for label, value in stats.items():
            self.ax_stats.text(0.05, y_pos, f'{label}:', fontsize=10, 
                              color='lightgray', fontweight='bold')
            self.ax_stats.text(0.55, y_pos, str(value), fontsize=10, 
                              color=self.indicator_colors.get(self.current_indicator, 'white'))
            y_pos -= 0.12
        
        self.ax_stats.set_xlim(0, 1)
        self.ax_stats.set_ylim(0, 1)
        self.ax_stats.set_xticks([])
        self.ax_stats.set_yticks([])
        
        # Distribution panel (histogram)
        self.ax_dist.set_facecolor('#1a1a2e')
        self.ax_dist.hist(current_data, bins=20, 
                         color=self.indicator_colors.get(self.current_indicator, 'white'),
                         alpha=0.7, edgecolor='white', linewidth=0.5)
        self.ax_dist.set_title('Distribution', fontsize=10, color='white', fontweight='bold')
        self.ax_dist.tick_params(colors='white', labelsize=8)
        self.ax_dist.grid(True, alpha=0.3)
        
        # Remove axes for cleaner look
        for spine in self.ax_stats.spines.values():
            spine.set_visible(False)
    
    def change_indicator(self, indicator):
        """Switch water quality indicator"""
        print(f"Switched to indicator: {indicator}")
        
        # Update button colors
        for ind in self.indicators:
            if ind in self.buttons:
                if ind == indicator:
                    self.buttons[ind].color = '#FFFFFF'
                    self.buttons[ind].label.set_color('black')
                else:
                    self.buttons[ind].color = self.indicator_colors.get(ind, '#888888')
                    self.buttons[ind].label.set_color('white')
        
        self.current_indicator = indicator
        self.update_visualization()
    
    def change_mode(self, mode):
        """Switch art mode"""
        print(f"Switched to mode: {mode}")
        
        # Update mode button colors
        modes = ['galaxy', 'particle', 'wave', 'energy']
        for m in modes:
            button_key = f'mode_{m}'
            if button_key in self.buttons:
                if m == mode:
                    self.buttons[button_key].color = '#FFD700'
                else:
                    self.buttons[button_key].color = '#444444'
        
        self.current_mode = mode
        self.update_visualization()
    
    def update_visualization(self):
        """Update main visualization"""
        # Stop previous animation
        if self.ani:
            self.ani.event_source.stop()
        
        # Clear main canvas
        self.ax_main.clear()
        
        # Update data panels
        self.update_data_panels()
        
        # Set main plot style
        self.ax_main.set_facecolor('#0a0a1a')
        self.ax_main.set_xlim(-10, 10)
        self.ax_main.set_ylim(-8, 8)
        self.ax_main.set_xticks([])
        self.ax_main.set_yticks([])
        
        # Hide borders
        for spine in self.ax_main.spines.values():
            spine.set_visible(False)
        
        # Get current data
        data = self.df[self.current_indicator].values
        self.normalized_data = self.normalize(data)
        
        # Set enhanced title with data info
        current_stats = self.df[self.current_indicator]
        mode_names = {
            'galaxy': 'Galaxy Mode',
            'particle': 'Enhanced Particle Mode',
            'wave': 'Wave Mode', 
            'energy': 'Energy Field Mode'
        }
        
        title = f'{self.current_indicator} - {mode_names.get(self.current_mode)}\n'
        title += f'Range: {current_stats.min():.1f} - {current_stats.max():.1f} | '
        title += f'Mean: {current_stats.mean():.2f} | Samples: {len(current_stats)}'
        
        self.ax_main.set_title(title, fontsize=16, color='white', fontweight='bold', pad=20)
        
        # Initialize based on mode
        if self.current_mode == 'galaxy':
            self.init_galaxy()
        elif self.current_mode == 'particle':
            self.init_enhanced_particle()  # Enhanced particle mode
        elif self.current_mode == 'wave':
            self.init_wave()
        elif self.current_mode == 'energy':
            self.init_energy_field()
        
        # Start animation
        self.frame = 0
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, frames=1000, 
            interval=60, blit=False, repeat=True
        )
        
        plt.draw()
    
    def init_galaxy(self):
        """Initialize enhanced galaxy mode"""
        n_points = min(len(self.normalized_data), 1000)  # Limit for performance
        
        # Create multiple spiral arms based on data quartiles
        indices = np.linspace(0, len(self.normalized_data)-1, n_points, dtype=int)
        selected_data = self.normalized_data[indices]
        
        # Create spiral coordinates with data-driven radius
        t = np.linspace(0, 6 * np.pi, n_points)
        r = 2 + 4 * selected_data  # Radius varies with data values
        
        self.x = r * np.cos(t) + np.random.normal(0, 0.3, n_points)
        self.y = r * np.sin(t) + np.random.normal(0, 0.3, n_points)
        
        # Enhanced point styling
        sizes = selected_data * 80 + 20
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        # Create color gradient based on data values
        colors = plt.cm.get_cmap('viridis')(selected_data)
        
        self.scatter = self.ax_main.scatter(self.x, self.y, s=sizes, c=colors, 
                                          alpha=0.8, edgecolors=color, linewidths=1)
        
        # Enhanced central black hole with data-based size
        avg_value = np.mean(selected_data)
        hole_size = 0.5 + avg_value * 0.8
        center = Circle((0, 0), hole_size, color='black', alpha=0.9)
        self.ax_main.add_patch(center)
        
        # Add data value indicators around the galaxy
        for i in range(0, n_points, n_points//8):
            angle = t[i]
            text_x = (r[i] + 1) * np.cos(angle)
            text_y = (r[i] + 1) * np.sin(angle)
            original_idx = indices[i]
            value = self.df[self.current_indicator].iloc[original_idx]
            self.ax_main.text(text_x, text_y, f'{value:.1f}', 
                            fontsize=8, color='white', alpha=0.7,
                            ha='center', va='center')
    
    def init_enhanced_particle(self):
        """Initialize enhanced particle mode with better data representation"""
        n_points = min(len(self.normalized_data), 800)
        indices = np.linspace(0, len(self.normalized_data)-1, n_points, dtype=int)
        selected_data = self.normalized_data[indices]
        
        # Create clusters based on data value ranges
        low_mask = selected_data < 0.33
        mid_mask = (selected_data >= 0.33) & (selected_data < 0.67)
        high_mask = selected_data >= 0.67
        
        # Position particles based on data ranges
        self.x = np.zeros(n_points)
        self.y = np.zeros(n_points)
        
        # Low values: left side
        self.x[low_mask] = np.random.uniform(-8, -2, np.sum(low_mask))
        self.y[low_mask] = np.random.uniform(-6, 6, np.sum(low_mask))
        
        # Medium values: center
        self.x[mid_mask] = np.random.uniform(-2, 2, np.sum(mid_mask))
        self.y[mid_mask] = np.random.uniform(-4, 4, np.sum(mid_mask))
        
        # High values: right side  
        self.x[high_mask] = np.random.uniform(2, 8, np.sum(high_mask))
        self.y[high_mask] = np.random.uniform(-6, 6, np.sum(high_mask))
        
        # Data-driven velocities
        self.vx = (selected_data - 0.5) * 0.3
        self.vy = np.random.uniform(-0.15, 0.15, n_points)
        
        # Enhanced particle styling
        sizes = selected_data * 100 + 30
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax_main.scatter(self.x, self.y, s=sizes, c=color, 
                                          alpha=0.7, edgecolors='white', linewidths=1)
        
        # Add data range labels
        self.ax_main.text(-6, -7, 'Low Values', fontsize=12, color='lightblue', 
                         fontweight='bold', ha='center')
        self.ax_main.text(0, -7, 'Medium Values', fontsize=12, color='yellow', 
                         fontweight='bold', ha='center')
        self.ax_main.text(6, -7, 'High Values', fontsize=12, color='orange', 
                         fontweight='bold', ha='center')
        
        # Store data for animation
        self.particle_data = selected_data
        self.particle_indices = indices
    
    def init_wave(self):
        """Initialize enhanced wave mode"""
        x = np.linspace(-10, 10, len(self.normalized_data))
        self.wave_x = x
        self.base_y = (self.normalized_data - 0.5) * 6  # Increased amplitude
        
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        # Main wave with data points
        self.line, = self.ax_main.plot(x, self.base_y, color=color, linewidth=4, alpha=0.9)
        
        # Add data points on the wave
        sample_indices = np.linspace(0, len(x)-1, 20, dtype=int)
        self.ax_main.scatter(x[sample_indices], self.base_y[sample_indices], 
                           s=80, c='white', edgecolors=color, linewidths=2, zorder=5)
        
        # Multi-layer waves with different frequencies
        self.wave_lines = []
        for i in range(4):
            frequency = 0.5 + i * 0.2
            line, = self.ax_main.plot(x, self.base_y + i*0.8, 
                                    color=color, linewidth=3-i*0.5, 
                                    alpha=0.7-i*0.15)
            self.wave_lines.append(line)
    
    def init_energy_field(self):
        """Initialize energy field mode - electromagnetic field visualization"""
        n_points = min(len(self.normalized_data), 600)
        indices = np.linspace(0, len(self.normalized_data)-1, n_points, dtype=int)
        selected_data = self.normalized_data[indices]
        
        # Create energy field nodes based on data values
        # High energy nodes (high data values) in center
        # Lower energy distributed around
        
        # Create grid-based energy field
        grid_size = int(np.sqrt(n_points))
        x_grid = np.linspace(-8, 8, grid_size)
        y_grid = np.linspace(-6, 6, grid_size)
        
        self.field_x = []
        self.field_y = []
        self.field_energies = []
        
        for i, energy in enumerate(selected_data[:grid_size*grid_size]):
            row = i // grid_size
            col = i % grid_size
            
            # Base position on grid
            base_x = x_grid[col]
            base_y = y_grid[row]
            
            # Distort position based on energy level
            distortion = energy * 2
            angle = energy * 4 * np.pi
            
            final_x = base_x + distortion * np.cos(angle)
            final_y = base_y + distortion * np.sin(angle)
            
            self.field_x.append(final_x)
            self.field_y.append(final_y)
            self.field_energies.append(energy)
        
        self.field_x = np.array(self.field_x)
        self.field_y = np.array(self.field_y)
        self.field_energies = np.array(self.field_energies)
        
        # Create energy nodes with varying sizes and intensities
        sizes = self.field_energies * 120 + 40
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        # Use colormap for energy intensity
        energy_colors = plt.cm.plasma(self.field_energies)
        
        self.energy_nodes = self.ax_main.scatter(self.field_x, self.field_y, 
                                               s=sizes, c=energy_colors, 
                                               alpha=0.8, edgecolors=color, linewidths=2)
        
        # Create energy field lines connecting high-energy nodes
        self.field_lines = []
        energy_threshold = np.percentile(self.field_energies, 70)  # Top 30% energy nodes
        
        high_energy_indices = np.where(self.field_energies > energy_threshold)[0]
        
        # Connect high-energy nodes with field lines
        for i, idx1 in enumerate(high_energy_indices[:-1]):
            for idx2 in high_energy_indices[i+1:i+4]:  # Connect to next 3 nodes max
                if idx1 != idx2:
                    x1, y1 = self.field_x[idx1], self.field_y[idx1]
                    x2, y2 = self.field_x[idx2], self.field_y[idx2]
                    
                    # Only draw line if nodes are reasonably close
                    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if distance < 6:
                        line_alpha = (self.field_energies[idx1] + self.field_energies[idx2]) / 2
                        line, = self.ax_main.plot([x1, x2], [y1, y2], 
                                                color=color, alpha=line_alpha*0.6, 
                                                linewidth=2, linestyle='--')
                        self.field_lines.append(line)
        
        # Add central energy core
        core_energy = np.mean(self.field_energies)
        core_size = core_energy * 200 + 100
        self.energy_core = self.ax_main.scatter([0], [0], s=core_size, 
                                              c='white', alpha=0.9, 
                                              edgecolors=color, linewidths=3,
                                              marker='*')
        
        # Add energy level indicators
        max_energy_idx = np.argmax(self.field_energies)
        min_energy_idx = np.argmin(self.field_energies)
        
        max_val = self.df[self.current_indicator].iloc[indices[max_energy_idx]]
        min_val = self.df[self.current_indicator].iloc[indices[min_energy_idx]]
        
        self.ax_main.text(self.field_x[max_energy_idx], self.field_y[max_energy_idx] + 1, 
                         f'Max: {max_val:.1f}', fontsize=10, color='yellow', 
                         fontweight='bold', ha='center')
        self.ax_main.text(self.field_x[min_energy_idx], self.field_y[min_energy_idx] - 1, 
                         f'Min: {min_val:.1f}', fontsize=10, color='cyan', 
                         fontweight='bold', ha='center')
        
        # Store for animation
        self.energy_base_x = self.field_x.copy()
        self.energy_base_y = self.field_y.copy()
    
    def animate(self, frame_num):
        """Enhanced animation with better effects"""
        self.frame += 1
        
        if self.current_mode == 'galaxy':
            return self.animate_galaxy()
        elif self.current_mode == 'particle':
            return self.animate_enhanced_particle()
        elif self.current_mode == 'wave':
            return self.animate_wave()
        elif self.current_mode == 'energy':
            return self.animate_energy_field()
        
        return []
    
    def animate_galaxy(self):
        """Enhanced galaxy animation with pulsing effect"""
        # Rotation with variable speed
        angle = self.frame * 0.015
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        
        self.scatter.set_offsets(np.column_stack([new_x, new_y]))
        
        # Pulsing effect based on data values
        pulse = 1 + 0.3 * np.sin(self.frame * 0.1)
        current_sizes = self.scatter.get_sizes() * pulse
        self.scatter.set_sizes(current_sizes)
        
        return [self.scatter]
    
    def animate_enhanced_particle(self):
        """Enhanced particle animation with data-driven behavior"""
        # Update positions with data-influenced movement
        attraction_strength = 0.02
        
        # Attract particles towards their data-appropriate regions
        target_x = np.where(self.particle_data < 0.33, -5,
                           np.where(self.particle_data < 0.67, 0, 5))
        
        # Apply gentle attraction
        self.vx += (target_x - self.x) * attraction_strength
        self.vy *= 0.99  # Slight damping
        
        # Update positions
        self.x += self.vx
        self.y += self.vy
        
        # Boundary conditions with wrapping
        self.x = np.where(self.x < -10, 10, np.where(self.x > 10, -10, self.x))
        self.y = np.where(self.y < -8, 8, np.where(self.y > 8, -8, self.y))
        
        self.scatter.set_offsets(np.column_stack([self.x, self.y]))
        
        # Size variation based on velocity
        speeds = np.sqrt(self.vx**2 + self.vy**2)
        dynamic_sizes = (self.particle_data * 80 + 30) * (1 + speeds * 2)
        self.scatter.set_sizes(dynamic_sizes)
        
        return [self.scatter]
    
    def animate_wave(self):
        """Enhanced wave animation with data-driven frequency"""
        wave_phase = self.frame * 0.15
        
        # Main wave with data-driven amplitude modulation
        data_modulation = 1 + 0.5 * np.sin(self.frame * 0.05)
        y = self.base_y * data_modulation + 3 * np.sin(self.wave_x * 0.4 + wave_phase)
        self.line.set_ydata(y)
        
        # Secondary waves with different phases
        for i, line in enumerate(self.wave_lines):
            phase_offset = i * np.pi / 4
            frequency = 0.4 + i * 0.1
            amplitude = 2 - i * 0.3
            y_wave = (self.base_y * (1 - i * 0.2) + 
                     amplitude * np.sin(self.wave_x * frequency + wave_phase + phase_offset))
            line.set_ydata(y_wave)
        
        return [self.line] + self.wave_lines
    
    def animate_energy_field(self):
        """Energy field animation with pulsing and field fluctuations"""
        # Energy field oscillation
        time_factor = self.frame * 0.1
        
        # Create energy waves that propagate through the field
        wave1 = np.sin(time_factor + self.field_energies * 8) * 0.3
        wave2 = np.cos(time_factor * 0.7 + self.field_energies * 5) * 0.2
        
        # Update node positions with energy-based oscillations
        new_x = self.energy_base_x + wave1 * self.field_energies
        new_y = self.energy_base_y + wave2 * self.field_energies
        
        self.energy_nodes.set_offsets(np.column_stack([new_x, new_y]))
        
        # Pulsing effect for node sizes
        pulse = 1 + 0.4 * np.sin(time_factor * 2 + self.field_energies * 10)
        base_sizes = self.field_energies * 120 + 40
        pulsing_sizes = base_sizes * pulse
        self.energy_nodes.set_sizes(pulsing_sizes)
        
        # Update energy core with strong pulsing
        core_pulse = 1 + 0.6 * np.sin(time_factor * 3)
        core_base_size = np.mean(self.field_energies) * 200 + 100
        core_size = core_base_size * core_pulse
        self.energy_core.set_sizes([core_size])
        
        # Animate field line transparency
        line_pulse = 0.3 + 0.4 * np.sin(time_factor * 1.5)
        for line in self.field_lines:
            line.set_alpha(line_pulse)
        
        # Update energy node colors with time-based shifting
        color_shift = (self.field_energies + time_factor * 0.1) % 1.0
        shifted_colors = plt.cm.plasma(color_shift)
        self.energy_nodes.set_color(shifted_colors)
        
        return [self.energy_nodes, self.energy_core] + self.field_lines
    
    def show(self):
        """Display the enhanced visualization"""
        plt.tight_layout()
        plt.show()

# Launch enhanced application
if __name__ == "__main__":
    print("Starting Enhanced Interactive Water Quality Art Visualization...")
    app = EnhancedWaterArtVisualization()
    app.show()