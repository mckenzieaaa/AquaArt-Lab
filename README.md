# Tide Height Visualization Script

This project provides a Python script for visualizing tide height data from an HTML file. The visualization features a static rainbow line that draws from left to right (time), with the y-axis (tide height) increasing from bottom to top. You can interactively inspect the data: when you hover your mouse over any part of the line, a tooltip will display the exact time and tide height at that location. This makes it easy to explore dense data and get precise values on demand.

## File Structure
- main.py: Main visualization script, parses HTML and animates the tide chart
- requirements.txt: Dependency list
- .gitignore: Ignore files that should not be version controlled
- README.md: Project description

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python main.py
   ```

## Dependencies
- beautifulsoup4
- matplotlib
- numpy

## Example
The script reads a file named `crawled-page-2023.html` and displays a rainbow-colored tide height line chart. The x-axis represents time, and the y-axis represents tide height (in meters). Hover your mouse over the line to see the exact time and tide height at any point. You can replace or modify the HTML file as needed for your own data.
