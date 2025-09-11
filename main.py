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

    # Plot points and lines
    ax.plot(date_objs, heights, marker='o', color='#0072B2', linewidth=2, markersize=5, label='Tide Height')

    # Beautify x-axis
    if isinstance(date_objs[0], datetime):
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        fig.autofmt_xdate(rotation=45)
    else:
        ax.set_xticks(range(0, len(dates), max(1, len(dates)//10)))
        ax.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//10))], rotation=45)

    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
