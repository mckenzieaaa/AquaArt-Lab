# AquaArt Lab

This project includes three main scripts for data visualization and artistic expression:

1. `main.py`: Visualizes tide height data from an HTML file provided by the instructor. The animation features a colorful, interactive tide chart. (Data: `crawled-page-2023.html`)
2. `plot_water_quality.py`: Performs standard analysis and charting of water quality data. (Data: `water_potability.csv`)
3. `plot_water_quality_art.py`: Transforms water quality indicators into animated, artistic shapes for creative data expression. (Data: `water_potability.csv`)

## File Structure
- main.py: Tide height visualization (uses instructor's HTML data)
- plot_water_quality.py: Standard water quality analysis and visualization (uses CSV data)
- plot_water_quality_art.py: Artistic animated water quality visualization (uses CSV data)
- crawled-page-2023.html: Instructor-provided tide height data
- water_potability.csv: Water quality dataset
- requirements.txt: Dependency list
- .gitignore: Ignore files that should not be version controlled
- README.md: Project description

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the tide visualization:
   ```bash
   python main.py
   ```
3. Run the standard water quality analysis:
   ```bash
   python plot_water_quality.py
   ```
4. Run the artistic water quality animation:
   ```bash
   python plot_water_quality_art.py
   ```

## Dependencies
- beautifulsoup4 (for tide data parsing)
- pandas
- matplotlib
- numpy
- seaborn

## Example
- Run `main.py` to see a colorful, interactive tide height animation using the instructor's HTML data.
- Run `plot_water_quality.py` for classic water quality analysis and charts using the CSV data.
- Run `plot_water_quality_art.py` to enjoy animated, creative shapes representing water quality indicators from the CSV data.
