'''
satplot.py

Description:
Plots the trajectory of a satellite given a TLE over a 1 day period

Requirements:
skyfield, pytz, basemap, numpy

Elston Almeida
2020
'''

from skyfield.api import EarthSatellite, load, Topos
import datetime, pytz
import numpy as np

# The resolution of the calculated path of the satellite
RES = 20000
# The host of the tle dataset
TLE_HOST = 'https://www.celestrak.com/NORAD/elements/active.txt'
# A specific satellite chosen from the tle dataset
SAT_CHOSEN = 'KEPLER-1 (CASE)'

# Get the tle data of the satellite chosen
tle_sats = load.tle_file(TLE_HOST)
print("loaded {} satellites from {}".format(len(tle_sats),TLE_HOST))
sats_by_name = {sat.name: sat for sat in tle_sats}   
sat_chosen = sats_by_name[SAT_CHOSEN]
print(sat_chosen)

# Get current time, end time, and time difference (delta) between each sample based on RES
ts = load.timescale()
ti = datetime.datetime.now(pytz.utc) # pytz.utc ensures utc encodding
tf = ti + datetime.timedelta(days=1)
delta = (tf - ti)/RES

latitude = []
longitude = []

# Using the delta calculated earlier, we find the longitude and latitude at a time
# t + \deta t then convert the dms values to decimal degrees which can help with plotting

t = ti
for i in range(RES):
    t += datetime.timedelta(seconds=delta.total_seconds())
    #convert a py datetime object to skyfield time object
    timeObj = ts.from_datetime(t) 
    # Get point data at a time given as timeObj
    point = sat_chosen.at(timeObj).subpoint()
    # Convert latitude and longitude to DMS
    clat = point.latitude.dms()
    clong = point.longitude.dms()
    # Convert DMS to DD and save in lists
    latitude.append(clat[0] + clat[1]/60 + clat[2]/3600)
    longitude.append(clong[0] + clong[1]/60 + clong[2]/3600)

# Ensure that the lists are of equal length before trying to plot
assert(len(latitude) == len(longitude))

# Plotting orbit data
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Using matplotlib's basemap to help provide cylindrical equidistant projection
fig =  plt.figure(figsize=(10,8), edgecolor='w')
m = Basemap(projection='cyl', resolution='c',
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-90,91,30))
m.drawmeridians(np.arange(-180,181,30))
m.drawmapboundary(fill_color='white')

# Plot latitude and longitude as a scatter plot onto the figure
m.scatter(longitude, latitude, latlon=True, s=1, c='green', zorder=2)
plt.show()