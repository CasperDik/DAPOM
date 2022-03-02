from strava_tool import load_data, total_duration, total_distance, speed_kmh, average_speed, min_max_speed
from plot_gpx import plot_gpx
from plot_gpx_folium import plot_gpx_folium

def execute():
    points = load_data("Ochtendrit.gpx")
    print(total_duration(points))
    print(total_distance(points))

    speed = speed_kmh(points)

    print(average_speed(speed))
    print(min_max_speed(speed))

    # plot_gpx(points, speed)
    plot_gpx_folium(points, speed)

if __name__ == '__main__':
    execute()

