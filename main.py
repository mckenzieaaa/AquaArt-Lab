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
                # 只取有潮高的行
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
    html_file = 'crawled-page-2023.html'
    dates, heights = parse_tide_heights(html_file)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_title('2023赤鱲角潮汐高度动画')
    ax.set_xlabel('观测点序号')
    ax.set_ylabel('潮高 (m)')
    ax.set_ylim(min(heights)-0.2, max(heights)+0.2)
    line, = ax.plot([], [], lw=2)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x = list(range(i+1))
        y = heights[:i+1]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(heights), interval=30, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
