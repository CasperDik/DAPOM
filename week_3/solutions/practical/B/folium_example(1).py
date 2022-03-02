import folium
import gpxpy.gpx
from geopy import distance


def generate_html_track_map():
    gpx_file = open('02-Sep-2019-1316.gpx', 'r')
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

    center_lat = (min(lats) + max(lats))/2
    center_lon = (min(lons) + max(lons))/2

    map = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    for i in range(len(points) - 1):
        distanceOfSegment = distance.distance((points[i][0], points[i][1]),
                                              (points[i + 1][0], points[i + 1][1])).meters
        durationOfSegment = points[i + 1][2] - points[i][2]
        speedOfSegment = distanceOfSegment / durationOfSegment.seconds / 1000 * 3600 # result in km/h

        if speedOfSegment < 4:
            folium.PolyLine([(points[i][0], points[i][1]),
                             (points[i + 1][0], points[i + 1][1])],
                            color='green', weight=5, opacity=0.4).add_to(map)
        if 4 <= speedOfSegment <= 7:
            folium.PolyLine([(points[i][0], points[i][1]),
                             (points[i + 1][0], points[i + 1][1])],
                            color='blue', weight=7, opacity=0.4).add_to(map)
        if speedOfSegment > 7:
            folium.PolyLine([(points[i][0], points[i][1]),
                             (points[i + 1][0], points[i + 1][1])],
                            color='red', weight=9, opacity=0.4).add_to(map)

    map.save("foliumExample.html")
    print("by using a browser, look at the map in the file foliumExample.html - in the project folder")


if __name__ == '__main__':
    generate_html_track_map()
