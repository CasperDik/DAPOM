# solution 5.6 with Smopy
# author: Nick Szirbik
# date: 23 Sept 2020
'''
read JSON data in a data DataFrame
collect the geolocation data from the data frame in lists
show taxi rides as pickup, dropoff connecting lines on a map
'''
import json
import pandas as pd
import smopy

import sys, os

taxi = pd.read_json(os.path.join(sys.path[0],"taxiRuns.json"),
                    orient = 'records')
#print(taxi.describe())

pminlon = taxi.pickup_location.apply(lambda lonlat: lonlat[0]).min()
dminlon = taxi.dropoff_location.apply(lambda lonlat: lonlat[0]).min()
minlon = min(pminlon, dminlon)
pminlat = taxi.pickup_location.apply(lambda lonlat: lonlat[1]).min()
dminlat = taxi.dropoff_location.apply(lambda lonlat: lonlat[1]).min()
minlat = min(pminlat, dminlat)
pmaxlon = taxi.pickup_location.apply(lambda lonlat: lonlat[0]).max()
dmaxlon = taxi.dropoff_location.apply(lambda lonlat: lonlat[0]).max()
maxlon = max(pmaxlon, dmaxlon)
pmaxlat = taxi.pickup_location.apply(lambda lonlat: lonlat[1]).max()
dmaxlat = taxi.dropoff_location.apply(lambda lonlat: lonlat[1]).max()
maxlat = max(pmaxlat, dmaxlat)

map = smopy.Map((minlat, minlon, maxlat, maxlon), z=12)
ax = map.show_mpl(figsize=(15, 15))

ppoints = taxi['pickup_location'].tolist()
dpoints = taxi['dropoff_location'].tolist()
for i in range(len(ppoints)):
    x1, y1 = map.to_pixels(ppoints[i][1], ppoints[i][0])
    ax.plot(x1, y1, 'or', color="red", ms=2, mew=1)
    x2, y2 = map.to_pixels(dpoints[i][1], dpoints[i][0])
    ax.plot(x2, y2, 'or', color="green", ms=2, mew=1)
    ax.plot([x1,x2], [y1,y2])

print("exit code 0")
