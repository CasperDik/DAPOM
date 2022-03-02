import folium
import pandas as pd
import branca.colormap as cm

def plot_gpx_folium(points, speed):
    lats = pd.Series([p[0] for p in points], name="lats")
    longs = pd.Series([p[1] for p in points], name="longs")

    # set up map
    m = folium.Map(location=[(min(lats) + max(lats))/2, (min(longs) + max(longs))/2], zoom_start=12, control_scale=True)

    # solutions 1:
    # lat_s = lats[0]
    # long_s = longs[0]
    # for lat, long in zip(lats[1:], longs[1:]):
    #     folium.PolyLine([(lat_s, long_s), (lat, long)], color='red', weight=15, opacity=0.8).add_to(m)
    #     lat_s = lat
    #     long_s = long

    # solution 2:
    # folium.PolyLine([zip(lats, longs)], color="blue", weight=5, opacity=0.8).add_to(m)

    # color map
    colormap = cm.linear.YlOrRd_09.scale(min(speed), max(speed)).to_step(len(speed))
    route = [[lat, lon] for lat, lon in zip(lats, longs)]
    folium.ColorLine(positions=route, colors=speed, colormap=colormap, weight=4, opacity=0.5).add_to(m)

    m.save("strava_folium_map.html")