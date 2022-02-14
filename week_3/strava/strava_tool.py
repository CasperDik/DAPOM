import gpxpy.gpx
from geopy import distance

# read gpx file
gpx_file = open("Ochtendrit.gpx", 'r')
gpx = gpxpy.parse(gpx_file)

# initiate empty list to store points
points = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # append latitude, longitude and time as a list to the list points
            points.append([point.latitude, point.longitude, point.time])

# total duration is end time - begin time
duration = points[-1][2] - points[0][2]
print("total duration of the activity in seconds: ", duration.seconds)

# distance between
p1, p2 = points[:2]
print("distance between first two points in meters: ", distance.distance((p1[0], p1[1]), (p2[0], p2[1])).meters)

# calculate total distance
total_distance = 0
for i in range(len(points)-1):
    total_distance += distance.distance((points[i][0], points[i][1]), (points[i+1][0], points[i+1][1])).meters

print("total distance in meters: ", total_distance)
print("total distance in km: ", total_distance/1000)
