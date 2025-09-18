# 交互式水质数据艺术可视化 - Interactive Water Quality Art
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import Circle
import random

class InteractiveWaterArt:
    def __init__(self):
        # 设置暗色主题
        plt.style.use('dark_background')
        
        # 创建主图和控制面板
        self.fig = plt.figure(figsize=(18, 12))
        
        # 主可视化区域 (占据大部分空间)
        self.ax_main = plt.subplot2grid((4, 6), (0, 0), colspan=6, rowspan=3)
        
        # 按钮控制区域 (底部)
        button_height = 0.06
        button_width = 0.12
        button_y = 0.02
        
        # 加载数据
        self.df = pd.read_csv('water_potability.csv')
        self.df = self.df.dropna()
        
        # 水质指标
        self.indicators = [col for col in self.df.columns if col != 'Potability']
        print(f"水质指标: {self.indicators}")
        
        # 当前选中的指标
        self.current_indicator = self.indicators[0]
        self.current_mode = 'galaxy'  # galaxy, particle, wave, network
        
        # 动画相关
        self.ani = None
        self.frame_count = 0
        
        # 颜色方案
        self.colors = {
            'ph': '#FF6B6B',           # 红色 - pH值
            'Hardness': '#4ECDC4',     # 青色 - 硬度
            'Solids': '#45B7D1',       # 蓝色 - 固体含量
            'Chloramines': '#96CEB4',  # 绿色 - 氯胺
            'Sulfate': '#FFEAA7',      # 黄色 - 硫酸盐
            'Conductivity': '#DDA0DD', # 紫色 - 导电率
            'Organic_carbon': '#98D8C8', # 浅绿 - 有机碳
            'Trihalomethanes': '#F7DC6F', # 浅黄 - 三卤甲烷
            'Turbidity': '#BB8FCE'     # 淡紫 - 浊度
        }
        
        # 创建按钮
        self.create_buttons()
        
        # 初始化可视化
        self.setup_visualization()
        
        print("交互式水质艺术可视化已准备就绪！")
    
    def create_buttons(self):
        """创建交互按钮"""
        self.buttons = {}
        
        # 指标选择按钮
        button_width = 0.10
        button_height = 0.04
        start_x = 0.05
        start_y = 0.25
        
        for i, indicator in enumerate(self.indicators):
            x = start_x + (i % 3) * (button_width + 0.02)
            y = start_y - (i // 3) * (button_height + 0.015)
            
            ax_button = plt.axes([x, y, button_width, button_height])
            button = Button(ax_button, indicator, 
                          color=self.colors.get(indicator, '#888888'),
                          hovercolor='white')
            button.on_clicked(lambda event, ind=indicator: self.switch_indicator(ind))
            self.buttons[f'indicator_{indicator}'] = button
        
        # 艺术效果模式按钮
        modes = [
            ('银河系', 'galaxy'),
            ('粒子流', 'particle'), 
            ('波纹', 'wave'),
            ('网络', 'network')
        ]
        
        mode_start_y = 0.12
        for i, (name, mode) in enumerate(modes):
            x = start_x + i * (button_width + 0.02)
            y = mode_start_y
            
            ax_button = plt.axes([x, y, button_width, button_height])
            button = Button(ax_button, name, 
                          color='#444444' if mode != self.current_mode else '#FFD700',
                          hovercolor='white')
            button.on_clicked(lambda event, m=mode: self.switch_mode(m))
            self.buttons[f'mode_{mode}'] = button
    
    def normalize_data(self, data):
        """标准化数据"""
        data = np.array(data)
        return (data - data.min()) / (data.max() - data.min() + 1e-8)
    
    def switch_indicator(self, indicator):
        """切换水质指标"""
        print(f"切换到指标: {indicator}")
        self.current_indicator = indicator
        self.setup_visualization()
    
    def switch_mode(self, mode):
        """切换艺术效果模式"""
        print(f"切换到模式: {mode}")
        self.current_mode = mode
        
        # 更新模式按钮颜色
        for mode_name in ['galaxy', 'particle', 'wave', 'network']:
            if f'mode_{mode_name}' in self.buttons:
                if mode_name == mode:
                    self.buttons[f'mode_{mode_name}'].color = '#FFD700'
                else:
                    self.buttons[f'mode_{mode_name}'].color = '#444444'
        
        self.setup_visualization()
    
    def setup_visualization(self):
        """设置可视化"""
        # 停止之前的动画
        if self.ani:
            self.ani.event_source.stop()
        
        # 清空主画布
        self.ax_main.clear()
        
        # 获取当前指标数据
        current_data = self.df[self.current_indicator]
        normalized_data = self.normalize_data(current_data)
        
        # 设置基本样式
        self.ax_main.set_facecolor('#0a0a1a')
        self.ax_main.set_xlim(-10, 10)
        self.ax_main.set_ylim(-8, 8)
        
        # 根据模式创建不同的可视化
        if self.current_mode == 'galaxy':
            self.create_galaxy_mode(normalized_data)
        elif self.current_mode == 'particle':
            self.create_particle_mode(normalized_data)
        elif self.current_mode == 'wave':
            self.create_wave_mode(normalized_data)
        elif self.current_mode == 'network':
            self.create_network_mode(normalized_data)
        
        # 设置标题和标签
        mode_names = {
            'galaxy': '银河系模式',
            'particle': '粒子流模式', 
            'wave': '波纹模式',
            'network': '网络模式'
        }
        
        title = f'{self.current_indicator} - {mode_names[self.current_mode]}'
        self.ax_main.set_title(title, fontsize=24, color='white', fontweight='bold', pad=20)
        
        # 移除坐标轴
        self.ax_main.set_xticks([])
        self.ax_main.set_yticks([])
        for spine in self.ax_main.spines.values():
            spine.set_visible(False)
        
        # 开始动画
        self.frame_count = 0
        self.ani = animation.FuncAnimation(self.fig, self.animate, 
                                         frames=1000, interval=50, 
                                         blit=False, repeat=True)
        
        plt.draw()
    
    def create_galaxy_mode(self, data):
        """创建银河系模式"""
        num_points = len(data)
        
        # 创建螺旋坐标
        t = np.linspace(0, 6 * np.pi, num_points)
        r = 1 + 4 * data  # 半径由数据决定
        
        self.galaxy_x = r * np.cos(t) + np.random.normal(0, 0.3, num_points)
        self.galaxy_y = r * np.sin(t) + np.random.normal(0, 0.3, num_points)
        
        # 点的属性
        sizes = data * 80 + 20
        color = self.colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax_main.scatter(self.galaxy_x, self.galaxy_y, 
                                          s=sizes, c=color, alpha=0.7,
                                          edgecolors='white', linewidths=0.5)
        
        # 添加中心黑洞
        center = Circle((0, 0), 0.5, color='black', alpha=0.9)
        self.ax_main.add_patch(center)
    
    def create_particle_mode(self, data):
        """创建粒子流模式"""
        num_points = len(data)
        
        # 随机初始位置
        self.particle_x = np.random.uniform(-8, 8, num_points)
        self.particle_y = np.random.uniform(-6, 6, num_points)
        
        # 速度由数据决定
        self.velocities = data * 0.2 + 0.05
        
        sizes = data * 60 + 15
        color = self.colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax_main.scatter(self.particle_x, self.particle_y,
                                          s=sizes, c=color, alpha=0.8)
    
    def create_wave_mode(self, data):
        """创建波纹模式"""
        x = np.linspace(-10, 10, len(data))
        self.wave_x = x
        self.wave_base_y = data * 4 - 2  # 基础高度由数据决定
        
        color = self.colors.get(self.current_indicator, '#888888')
        self.line, = self.ax_main.plot(x, self.wave_base_y, 
                                      color=color, linewidth=3, alpha=0.8)
        
        # 添加多层波纹效果
        self.wave_lines = []
        for i in range(5):
            line, = self.ax_main.plot(x, self.wave_base_y + i * 0.5, 
                                    color=color, linewidth=2-i*0.3, 
                                    alpha=0.6-i*0.1)
            self.wave_lines.append(line)
    
    def create_network_mode(self, data):
        """创建网络模式"""
        num_points = min(50, len(data))  # 限制点数以提高性能
        
        # 创建网格位置
        indices = np.linspace(0, len(data)-1, num_points, dtype=int)
        selected_data = data[indices]
        
        # 网格坐标
        grid_size = int(np.sqrt(num_points))
        if grid_size == 0:
            grid_size = 1
        
        actual_points = grid_size * grid_size
        x_pos = np.tile(np.linspace(-8, 8, grid_size), grid_size)[:actual_points]
        y_pos = np.repeat(np.linspace(-6, 6, grid_size), grid_size)[:actual_points]
        
        # 确保数据长度匹配
        selected_data = selected_data[:actual_points]
        
        self.network_x = x_pos
        self.network_y = y_pos
        self.network_data = selected_data
        
        # 绘制节点
        sizes = selected_data * 100 + 30
        color = self.colors.get(self.current_indicator, '#888888')
        
        self.scatter = self.ax_main.scatter(self.network_x, self.network_y,
                                          s=sizes, c=color, alpha=0.8,
                                          edgecolors='white', linewidths=1)
        
        # 绘制连接线（连接相似数值的点）
        self.network_lines = []
        threshold = 0.3
        for i in range(len(selected_data)):
            for j in range(i+1, len(selected_data)):
                if abs(selected_data[i] - selected_data[j]) < threshold:
                    line, = self.ax_main.plot([x_pos[i], x_pos[j]], 
                                            [y_pos[i], y_pos[j]], 
                                            color=color, alpha=0.3, linewidth=1)
                    self.network_lines.append(line)
    
    def animate(self, frame):
        """动画更新函数"""
        self.frame_count += 1
        
        if self.current_mode == 'galaxy':
            return self.animate_galaxy(frame)
        elif self.current_mode == 'particle':
            return self.animate_particle(frame)
        elif self.current_mode == 'wave':
            return self.animate_wave(frame)
        elif self.current_mode == 'network':
            return self.animate_network(frame)
        
        return []
    
    def animate_galaxy(self, frame):
        """银河系动画"""
        # 旋转效果
        angle = frame * 0.02
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        
        rotated_x = self.galaxy_x * cos_a - self.galaxy_y * sin_a
        rotated_y = self.galaxy_x * sin_a + self.galaxy_y * cos_a
        
        self.scatter.set_offsets(np.column_stack((rotated_x, rotated_y)))
        
        # 呼吸效果
        breathing = 1 + 0.2 * np.sin(frame * 0.1)
        current_sizes = self.scatter.get_sizes() * breathing
        self.scatter.set_sizes(current_sizes)
        
        return [self.scatter]
    
    def animate_particle(self, frame):
        """粒子流动画"""
        # 更新粒子位置
        angle_offset = frame * 0.05
        for i in range(len(self.particle_x)):
            angle = angle_offset + i * 0.1
            self.particle_x[i] += np.cos(angle) * self.velocities[i]
            self.particle_y[i] += np.sin(angle) * self.velocities[i] * 0.5
            
            # 边界处理
            if abs(self.particle_x[i]) > 8:
                self.particle_x[i] = -8 if self.particle_x[i] > 0 else 8
            if abs(self.particle_y[i]) > 6:
                self.particle_y[i] = -6 if self.particle_y[i] > 0 else 6
        
        self.scatter.set_offsets(np.column_stack((self.particle_x, self.particle_y)))
        return [self.scatter]
    
    def animate_wave(self, frame):
        """波纹动画"""
        # 创建波浪效果
        wave_offset = frame * 0.2
        
        # 主波浪
        y = self.wave_base_y + 2 * np.sin(self.wave_x * 0.5 + wave_offset)
        self.line.set_ydata(y)
        
        # 多层波纹
        for i, line in enumerate(self.wave_lines):
            phase_shift = i * np.pi / 4
            amplitude = 1.5 - i * 0.2
            y_layer = (self.wave_base_y + 
                      amplitude * np.sin(self.wave_x * 0.5 + wave_offset + phase_shift))
            line.set_ydata(y_layer)
        
        return [self.line] + self.wave_lines
    
    def animate_network(self, frame):
        """网络动画"""
        # 节点脉冲效果
        pulse = 1 + 0.3 * np.sin(frame * 0.1 + self.network_data * 10)
        current_sizes = (self.network_data * 100 + 30) * pulse
        self.scatter.set_sizes(current_sizes)
        
        # 连接线透明度变化
        alpha_base = 0.3 + 0.2 * np.sin(frame * 0.05)
        for line in self.network_lines:
            line.set_alpha(alpha_base)
        
        return [self.scatter] + self.network_lines
    
    def show(self):
        """显示可视化"""
        plt.tight_layout()
        plt.show()

# 创建并运行交互式可视化
if __name__ == "__main__":
    print("正在启动交互式水质艺术可视化...")
    art = InteractiveWaterArt()
    art.show()