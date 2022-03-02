import matplotlib.pyplot as plt
import smopy
import pandas as pd

def plot_gpx(points, speed):
    lats = pd.Series([p[0] for p in points], name="lats")
    longs = pd.Series([p[1] for p in points], name="longs")

    # to get similar lengths for speed
    lats = lats[1:-1]
    longs = longs[1:-1]

    # setup map
    map = smopy.Map((min(lats), min(longs), max(lats), max(longs)), z=12)
    # convert lats&longs to pixels
    x, y = map.to_pixels(lats, longs)

    ax = map.show_mpl(figsize=(10, 10))
    ax.scatter(x, y, s=5, c=speed, cmap="Reds")
    plt.show()
