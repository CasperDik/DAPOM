%reset -f

# This example implements the code for DAPOM practical 3B
# Wout van Wezel, 2020

import gpxpy
import gpxpy.gpx
from geopy import distance
import smopy

gpx_file = open('02-Sep-2019-1316.gpx', 'r') #remember you might need to explicitly add you path here
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

map = smopy.Map((min(lats), min(lons), max(lats), max(lons)), z=16)
ax = map.show_mpl(figsize=(10, 10))

for i in range(len(points)-1):
    x, y = map.to_pixels(points[i][0], points[i][1])
    distanceOfSegment = distance.distance((points[i][0],points[i][1]),(points[i+1][0],points[i+1][1])).meters
    durationOfSegment = points[i+1][2] - points[i][2]
    speedOfSegment = distanceOfSegment / durationOfSegment.seconds / 1000 * 3600
    if speedOfSegment<4:
        ax.plot(x, y, 'or', color="red", ms=2, mew=1);
    if speedOfSegment>=4 and speedOfSegment<=7:
        ax.plot(x, y, 'or', color="blue", ms=2, mew=1);
    if speedOfSegment>7:
        ax.plot(x, y, 'or', color="yellow", ms=2, mew=1);
