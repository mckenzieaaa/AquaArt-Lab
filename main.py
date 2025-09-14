import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def parse_tide_heights(html_file):
    with open(html_file, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    heights = []
    dates = []
    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 4:
                # Only process rows with tide height
                try:
                    date = f"{tds[0].text.strip()}-{tds[1].text.strip()}"
                    for i in range(3, len(tds), 2):
                        h = tds[i].text.strip().replace('\xa0','').replace('&nbsp;','')
                        if h:
                            try:
                                heights.append(float(h))
                                dates.append(date)
                            except ValueError:
                                pass
                except Exception:
                    pass
    return dates, heights

def main():
    import matplotlib.dates as mdates
    import matplotlib.font_manager as fm
    from datetime import datetime


    html_file = 'crawled-page-2023.html'
    dates, heights = parse_tide_heights(html_file)

    # Try to convert date strings to datetime objects for better x-axis formatting
    date_fmt = "%m月%d日-%H:%M"
    try:
        date_objs = [datetime.strptime(d, "%m月%d日-%H:%M") for d in dates]
    except Exception:
        date_objs = list(range(len(dates)))  # fallback


    # Set English font (for macOS, fallback to Arial)
    plt.rcParams['font.sans-serif'] = ['Arial', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title('2023 Chek Lap Kok Tide Height', fontsize=18, fontweight='bold')
    ax.set_xlabel('Date-Time', fontsize=14)
    ax.set_ylabel('Tide Height (m)', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Beautify x-axis
    if isinstance(date_objs[0], datetime):
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        fig.autofmt_xdate(rotation=45)
    else:
        ax.set_xticks(range(0, len(dates), max(1, len(dates)//10)))
        ax.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//10))], rotation=45)

    import numpy as np
    from matplotlib.collections import LineCollection

    # Prepare for rainbow color (x: time, y: height)
    x_vals = np.arange(len(heights))
    points = np.array([x_vals, heights]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(min(heights), max(heights))
    cmap = plt.get_cmap('rainbow')

    # For animation, we need to update a LineCollection
    line_collection = LineCollection([], cmap=cmap, norm=norm, linewidth=2, label='Tide Height')
    ax.add_collection(line_collection)

    # Annotation objects
    value_text = ax.text(0.98, 0.95, '', transform=ax.transAxes, ha='right', va='top', fontsize=13, color='black', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    point_annot = ax.annotate('', xy=(0,0), xytext=(10,10), textcoords='offset points', fontsize=12, color='black',
                              bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.7), arrowprops=dict(arrowstyle='->', color='gray'))
    point_annot.set_visible(False)

    def init():
        line_collection.set_segments([])
        line_collection.set_array(np.array([]))
        value_text.set_text('')
        point_annot.set_visible(False)
        return line_collection, value_text, point_annot

    def animate(i):
        if i == 0:
            value_text.set_text('')
            point_annot.set_visible(False)
            return line_collection, value_text, point_annot
        segs = segments[:i]
        # Use the y value (height) for each segment for coloring
        vals = [seg[0][1] for seg in segs] if len(segs) > 0 else []
        line_collection.set_segments(segs)
        line_collection.set_array(np.array(vals))

        # Annotate the latest point
        idx = i-1
        x = x_vals[idx]
        y = heights[idx]
        # Show time label if possible
        if isinstance(date_objs[0], datetime):
            time_str = date_objs[idx].strftime('%m-%d %H:%M')
        else:
            time_str = str(date_objs[idx])
        value_text.set_text(f'Time: {time_str}\nTide Height: {y:.2f} m')
        value_text.set_position((0.98, 0.95))
        # Place annotation at the latest point
        point_annot.xy = (x, y)
        point_annot.set_text(f'{time_str}\n{y:.2f} m')
        point_annot.set_visible(True)
        return line_collection, value_text, point_annot

    from matplotlib import animation
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(heights), interval=8, blit=True, repeat=False)
    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
