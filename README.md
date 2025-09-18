# AquaArt Lab 🌊✨

**Transform water quality data into stunning artistic animations!**

This project perfectly combines data science with artistic creativity, offering multiple water quality data visualization solutions:

## 🎨 Main Features

### 📊 Standard Analysis Tools
1. **`main.py`** - Tide Height Visualization: Creates colorful interactive tide charts from HTML data
2. **`plot_water_quality.py`** - Standard Water Quality Analysis: Classic statistical charts and analysis

### 🎭 Artistic Visualization Series
3. **`plot_water_quality_art.py`** - Particle Flow Art: Transforms water quality indicators into dynamic particle flow animations
4. **`water_quality_galaxy.py`** - Galaxy Art: Creates cosmic galaxy-style water quality data visualizations
5. **`interactive_water_art_v2.py`** - **🌟 Interactive Art Panel**:
   - 🎛️ Click to switch between 9 water quality indicators
   - 🎨 4 artistic effect modes (Galaxy, Particle, Wave, Spiral)
   - 🔄 Real-time animation effects
   - 🌈 Dedicated color scheme for each indicator

## 📁 Project Structure

### 🔧 Core Files
- **`main.py`** - Tide height visualization (using HTML data)
- **`plot_water_quality.py`** - Standard water quality analysis and visualization (using CSV data)

### 🎨 Artistic Visualization Series
- **`plot_water_quality_art.py`** - Particle flow art animation
- **`water_quality_galaxy.py`** - Galaxy-style art animation  
- **`interactive_water_art_v2.py`** - **🌟 Interactive Art Panel (Recommended)**
- **`interactive_water_art.py`** - Interactive Art Panel (Original Version)

### 📊 Data Files
- **`crawled-page-2023.html`** - Tide height data
- **`water_potability.csv`** - Water quality dataset

### ⚙️ Configuration Files
- **`requirements.txt`** - Dependencies list
- **`.gitignore`** - Git ignore file configuration
- **`README.md`** - Project documentation

## 🚀 Quick Start

### 📦 Environment Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure Python environment (if using virtual environment)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 🎯 Running Programs

#### 🌟 Recommended: Interactive Art Panel
```bash
python interactive_water_art_v2.py
```
**Key Features:**
- Left buttons to switch water quality indicators (pH, Hardness, Solids, etc.)
- Right buttons to switch art effects (Galaxy, Particle, Wave, Spiral)
- Real-time animations and color changes

#### 🎨 Other Art Effects
```bash
# Galaxy-style animation
python water_quality_galaxy.py

# Particle flow animation
python plot_water_quality_art.py
```

#### 📊 Standard Analysis
```bash
# Tide visualization
python main.py

# Water quality data analysis
python plot_water_quality.py
```

## 🔧 Tech Stack
- **`pandas`** - Data processing and analysis
- **`matplotlib`** - Plotting and animation
- **`numpy`** - Numerical computing
- **`beautifulsoup4`** - HTML data parsing
- **`seaborn`** - Statistical chart enhancement

## 🎮 Interactive Features Demo

### 🌟 `interactive_water_art_v2.py` - Main Features
- **9 Water Quality Indicators**: pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, Turbidity
- **4 Art Modes**:
  - 🌌 **Galaxy** - Spiral arm rotation with central black hole effect
  - ✨ **Particle** - Dynamic particle collision and flow
  - 🌊 **Wave** - Multi-layer wave animation effects  
  - 🌀 **Spiral** - Double helix DNA-style rotation

### 📊 Data Mapping Rules
- **Point Size** ← Data value magnitude
- **Color Scheme** ← Dedicated color for each indicator
- **Animation Trajectory** ← Data characteristics drive movement patterns
- **Transparency** ← Data intensity affects visual effects

## 🎨 Effect Preview
Run different programs to experience:
- **Tide Data Art** - Colorful interactive tide height animations
- **Water Quality Standard Analysis** - Classic statistical charts and data insights  
- **Particle Flow Art** - Water quality indicator-driven particle animations
- **Galaxy Art** - Cosmic-style water quality data visualization
- **Interactive Panel** - Real-time switchable multi-mode art effects

---
**✨ Turn data into art, make science beautiful!**
