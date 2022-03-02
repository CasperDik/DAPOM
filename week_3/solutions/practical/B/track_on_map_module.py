# This example implements the code for DAPOM practical 3 Big Data part
# Wout van Wezel, 2020

import gpxpy.gpx
from geopy import distance
import smopy
from matplotlib import pyplot as plt


def visualize_track_and_speed(file_name):
    gpx_file = open(file_name, 'r')
    gpx = gpxpy.parse(gpx_file)

    points = []
    lats = []
    lons = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append([point.latitude, point.longitude, point.time])
                lats.append(point.latitude)
                lons.append(point.longitude)

    map = smopy.Map((min(lats), min(lons), max(lats), max(lons)), z=18)
    matplotlib_map = map.show_mpl(figsize=(9, 9))

    for i in range(len(points)-1):
        x, y = map.to_pixels(points[i][0], points[i][1])
        distanceOfSegment = distance.distance((points[i][0],points[i][1]),(points[i+1][0],points[i+1][1])).meters
        durationOfSegment = points[i+1][2] - points[i][2]
        speedOfSegment = distanceOfSegment / durationOfSegment.seconds / 1000 * 3600
        if speedOfSegment < 4:
            matplotlib_map.plot(x, y, 'or', color="r", ms=2, mew=1)
        if 4 <= speedOfSegment <= 7:
            matplotlib_map.plot(x, y, 'or', color="b", ms=2, mew=1)
        if speedOfSegment > 7:
            matplotlib_map.plot(x, y, 'or', color="y", ms=2, mew=1)
    plt.show()
