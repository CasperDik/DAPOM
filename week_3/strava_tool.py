import gpxpy.gpx
from geopy import distance


def load_data(filename):
    # read gpx file
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    # initiate empty list to store points
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # append latitude, longitude and time as a list to the list points
                points.append([point.latitude, point.longitude, point.time])

    return points

def total_duration(points):
    # total duration is end time - begin time
    duration = points[-1][2] - points[0][2]
    # print("total duration of the activity in seconds: ", duration.seconds)

    return duration.seconds

def total_distance(points):
    # calculate total distance in meters

    total_distance = 0
    for i in range(len(points)-1):
        total_distance += distance.distance((points[i][0], points[i][1]), (points[i+1][0], points[i+1][1])).meters

    # print("total distance in meters: ", total_distance)
    # print("total distance in km: ", total_distance/1000)

    return total_distance

def speed_kmh(points):
    # calculate speed in km/h
    # speed = distance traveled / time elapsed
    speed = []

    for i in range(1, len(points)-1):
        distance_travelled = distance.distance((points[i][0], points[i][1]), (points[i-1][0], points[i-1][1])).meters
        time_elapsed = points[i][2] - points[i-1][2]
        speed.append(distance_travelled / time_elapsed.seconds * 3.6)

    return speed

def average_speed(list_speed):
    # calculated average speed from a list

    return sum(list_speed) / len(list_speed)

def min_max_speed(list_speed):
    # find max and min speed from a list

    return min(list_speed), max(list_speed)

if __name__ == "__main__":
    points = load_data("Ochtendrit.gpx")
    speed = speed_kmh(points)

    print(average_speed(speed))
