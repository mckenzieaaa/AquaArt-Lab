# Interactive Water Quality Art Visualization - Optimized Version
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import Circle

class WaterArtVisualization:
    def __init__(self):
        plt.style.use('dark_background')
        
        # Create figure and layout
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        
        # Load data
        self.df = pd.read_csv('water_potability.csv')
        self.df = self.df.dropna()
        
        # Water quality indicators
        self.indicators = [col for col in self.df.columns if col != 'Potability']
        self.current_indicator = self.indicators[0]
        self.current_mode = 'galaxy'
        
        # Color scheme
        self.indicator_colors = {
            'ph': '#FF6B6B',           # Red
            'Hardness': '#4ECDC4',     # Cyan  
            'Solids': '#45B7D1',       # Blue
            'Chloramines': '#96CEB4',  # Green
            'Sulfate': '#FFEAA7',      # Yellow
            'Conductivity': '#DDA0DD', # Purple
            'Organic_carbon': '#98D8C8', # Light green
            'Trihalomethanes': '#F7DC6F', # Light yellow
            'Turbidity': '#BB8FCE'     # Light purple
        }
        
        # Animation control
        self.ani = None
        self.frame = 0
        
        # Create control panel
        self.create_control_panel()
        
        # Initialize visualization
        self.update_visualization()
        
        print("Interactive Water Quality Art Visualization started!")
        print("Click left buttons to switch water quality indicators, right buttons to switch art effects")
    
    def normalize(self, data):
        """Data normalization"""
        data = np.array(data)
        return (data - data.min()) / (data.max() - data.min() + 1e-8)
    
    def create_control_panel(self):
        """Create control buttons"""
        self.buttons = {}
        
        # Adjust main plot position to leave space on the right
        self.fig.subplots_adjust(left=0.25, bottom=0.1, right=0.95, top=0.9)
        
        # Water quality indicator buttons (left side)
        button_height = 0.06
        button_width = 0.15
        start_y = 0.85
        
        for i, indicator in enumerate(self.indicators):
            y_pos = start_y - i * (button_height + 0.01)
            ax_button = self.fig.add_axes([0.05, y_pos, button_width, button_height])
            
            # Button color
            color = self.indicator_colors.get(indicator, '#888888')
            if indicator == self.current_indicator:
                color = 'white'
            
            button = Button(ax_button, indicator, color=color, hovercolor='lightgray')
            button.on_clicked(lambda x, ind=indicator: self.change_indicator(ind))
            self.buttons[indicator] = button
        
        # Art mode buttons (right side)
        modes = [
            ('Galaxy', 'galaxy'),
            ('Particle', 'particle'), 
            ('Wave', 'wave'),
            ('Spiral', 'spiral')
        ]
        
        for i, (name, mode) in enumerate(modes):
            y_pos = start_y - i * (button_height + 0.01)
            ax_button = self.fig.add_axes([0.97, y_pos, button_width, button_height])
            
            color = 'white' if mode == self.current_mode else '#555555'
            button = Button(ax_button, name, color=color, hovercolor='lightgray')
            button.on_clicked(lambda x, m=mode: self.change_mode(m))
            self.buttons[f'mode_{mode}'] = button
    
    def change_indicator(self, indicator):
        """Switch water quality indicator"""
        print(f"Switched to indicator: {indicator}")
        
        # Update button colors
        for ind in self.indicators:
            if ind in self.buttons:
                if ind == indicator:
                    self.buttons[ind].color = 'white'
                else:
                    self.buttons[ind].color = self.indicator_colors.get(ind, '#888888')
        
        self.current_indicator = indicator
        self.update_visualization()
    
    def change_mode(self, mode):
        """Switch art mode"""
        print(f"Switched to mode: {mode}")
        
        # Update mode button colors
        modes = ['galaxy', 'particle', 'wave', 'spiral']
        for m in modes:
            button_key = f'mode_{m}'
            if button_key in self.buttons:
                if m == mode:
                    self.buttons[button_key].color = 'white'
                else:
                    self.buttons[button_key].color = '#555555'
        
        self.current_mode = mode
        self.update_visualization()
    
    def update_visualization(self):
        """Update visualization"""
        # Stop previous animation
        if self.ani:
            self.ani.event_source.stop()
        
        # Clear canvas
        self.ax.clear()
        
        # Set style
        self.ax.set_facecolor('#0a0a1a')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-8, 8)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Hide borders
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        
        # Get current data
        data = self.df[self.current_indicator].values
        self.normalized_data = self.normalize(data)
        
        # Set title
        mode_names = {
            'galaxy': 'Galaxy Mode',
            'particle': 'Particle Mode',
            'wave': 'Wave Mode', 
            'spiral': 'Spiral Mode'
        }
        
        title = f'{self.current_indicator} - {mode_names.get(self.current_mode, self.current_mode)}'
        self.ax.set_title(title, fontsize=20, color='white', fontweight='bold', pad=20)
        
        # Initialize based on mode
        if self.current_mode == 'galaxy':
            self.init_galaxy()
        elif self.current_mode == 'particle':
            self.init_particle()
        elif self.current_mode == 'wave':
            self.init_wave()
        elif self.current_mode == 'spiral':
            self.init_spiral()
        
        # Start animation
        self.frame = 0
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, frames=1000, 
            interval=80, blit=False, repeat=True
        )
        
        plt.draw()
    
    def init_galaxy(self):
        """Initialize galaxy mode"""
        n_points = len(self.normalized_data)
        
        # Create spiral arms
        t = np.linspace(0, 4 * np.pi, n_points)
        r = 1 + 3 * self.normalized_data
        
        self.x = r * np.cos(t) + np.random.normal(0, 0.2, n_points)
        self.y = r * np.sin(t) + np.random.normal(0, 0.2, n_points)
        
        # Point size and color
        sizes = self.normalized_data * 60 + 20
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax.scatter(self.x, self.y, s=sizes, c=color, 
                                     alpha=0.7, edgecolors='white', linewidths=0.5)
        
        # Central black hole
        center = Circle((0, 0), 0.8, color='black', alpha=0.8)
        self.ax.add_patch(center)
    
    def init_particle(self):
        """Initialize particle mode"""
        n_points = len(self.normalized_data)
        
        # Random initial positions
        self.x = np.random.uniform(-8, 8, n_points)
        self.y = np.random.uniform(-6, 6, n_points)
        
        # Velocity
        self.vx = (self.normalized_data - 0.5) * 0.2
        self.vy = np.random.uniform(-0.1, 0.1, n_points)
        
        sizes = self.normalized_data * 40 + 10
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax.scatter(self.x, self.y, s=sizes, c=color, alpha=0.8)
    
    def init_wave(self):
        """Initialize wave mode"""
        x = np.linspace(-10, 10, len(self.normalized_data))
        self.wave_x = x
        self.base_y = (self.normalized_data - 0.5) * 4
        
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        self.line, = self.ax.plot(x, self.base_y, color=color, linewidth=3, alpha=0.9)
        
        # Multi-layer waves
        self.wave_lines = []
        for i in range(3):
            line, = self.ax.plot(x, self.base_y + i*0.5, 
                               color=color, linewidth=2-i*0.5, alpha=0.6-i*0.15)
            self.wave_lines.append(line)
    
    def init_spiral(self):
        """Initialize spiral mode"""
        n_points = len(self.normalized_data)
        
        # Double helix structure
        t = np.linspace(0, 6 * np.pi, n_points)
        r = 0.5 + 2 * self.normalized_data
        
        self.x1 = r * np.cos(t)
        self.y1 = r * np.sin(t)
        self.x2 = r * np.cos(t + np.pi)  # Reverse spiral
        self.y2 = r * np.sin(t + np.pi)
        
        sizes = self.normalized_data * 50 + 15
        color = self.indicator_colors.get(self.current_indicator, '#888888')
        
        self.scatter1 = self.ax.scatter(self.x1, self.y1, s=sizes, c=color, alpha=0.7)
        self.scatter2 = self.ax.scatter(self.x2, self.y2, s=sizes, c=color, alpha=0.5)
    
    def animate(self, frame_num):
        """Animation update"""
        self.frame += 1
        
        if self.current_mode == 'galaxy':
            return self.animate_galaxy()
        elif self.current_mode == 'particle':
            return self.animate_particle()
        elif self.current_mode == 'wave':
            return self.animate_wave()
        elif self.current_mode == 'spiral':
            return self.animate_spiral()
        
        return []
    
    def animate_galaxy(self):
        """Galaxy animation"""
        # Rotation
        angle = self.frame * 0.02
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        
        self.scatter.set_offsets(np.column_stack([new_x, new_y]))
        
        return [self.scatter]
    
    def animate_particle(self):
        """Particle animation"""
        # Update positions
        self.x += self.vx
        self.y += self.vy
        
        # Boundary bounce
        self.vx = np.where((self.x < -8) | (self.x > 8), -self.vx, self.vx)
        self.vy = np.where((self.y < -6) | (self.y > 6), -self.vy, self.vy)
        
        self.scatter.set_offsets(np.column_stack([self.x, self.y]))
        
        return [self.scatter]
    
    def animate_wave(self):
        """Wave animation"""
        wave_phase = self.frame * 0.2
        
        # Main wave
        y = self.base_y + 2 * np.sin(self.wave_x * 0.5 + wave_phase)
        self.line.set_ydata(y)
        
        # Additional waves
        for i, line in enumerate(self.wave_lines):
            phase_offset = i * np.pi / 3
            amplitude = 1.5 - i * 0.3
            y_wave = self.base_y + amplitude * np.sin(self.wave_x * 0.5 + wave_phase + phase_offset)
            line.set_ydata(y_wave)
        
        return [self.line] + self.wave_lines
    
    def animate_spiral(self):
        """Spiral animation"""
        # Double helix rotation
        angle1 = self.frame * 0.03
        angle2 = self.frame * 0.03 + np.pi
        
        cos_a1, sin_a1 = np.cos(angle1), np.sin(angle1)
        cos_a2, sin_a2 = np.cos(angle2), np.sin(angle2)
        
        new_x1 = self.x1 * cos_a1 - self.y1 * sin_a1
        new_y1 = self.x1 * sin_a1 + self.y1 * cos_a1
        
        new_x2 = self.x2 * cos_a2 - self.y2 * sin_a2
        new_y2 = self.x2 * sin_a2 + self.y2 * cos_a2
        
        self.scatter1.set_offsets(np.column_stack([new_x1, new_y1]))
        self.scatter2.set_offsets(np.column_stack([new_x2, new_y2]))
        
        return [self.scatter1, self.scatter2]
    
    def show(self):
        """Show visualization"""
        plt.show()

# Launch application
if __name__ == "__main__":
    print("Starting Interactive Water Quality Art Visualization...")
    app = WaterArtVisualization()
    app.show()