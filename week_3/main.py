from strava_tool import load_data, total_duration, total_distance, speed, average_speed, min_max_speed
from plot_gpx import plot_gpx

points = load_data("Ochtendrit.gpx")
print(total_duration(points))
print(total_distance(points))

speed = speed(points)

print(average_speed(speed))
print(min_max_speed(speed))

plot_gpx(points)

