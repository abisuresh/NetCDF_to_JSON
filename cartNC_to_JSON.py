import warnings 
warnings.simplefilter("ignore")
import os
import netCDF4
import json
import datetime
import pyart
from funcs import read_casa_netcdf

# dataset = netCDF4.Dataset("xmdl_grid.nc", "r")
dataset = pyart.io.grid_io.read_grid("xmdl_grid.nc", "r")
radar = pyart.io.read('xmdl_cfradial.nc')
# grid = pyart.map.grid_from_radars(
#     (radar,),
#     grid_shape = (1, 1600, 1600), # the resolution we're asking for is 1600 x 1600; could use smaller if needed?
#     # grid limits: ((min_height, max_height), (min_x, max_x), (min_y, max_y)) all in meters
#     grid_limits = ((501,1000), (-41000.0,41000.0), (-41000.0,41000.0)),
#     fields = ['Reflectivity','SignalToNoiseRatio']
# )

dimensions = dataset.dimensions
variables = dataset.variables

time = variables["time"]
snr = variables["SignalToNoiseRatio"]
latitude = variables["origin_latitude"]
longitude = variables["origin_longitude"]
reflectivity = variables["Reflectivity"]
x_value = variables["x"]
y_value = variables["y"]

times = []
isotimes = []
snrs = []

# for x in range(0, 1600): 
beam = snr[0].tolist()
snrs.append(beam)
t = time[time[0]].tolist()
times.append(t)
isotimes.append(datetime.datetime.fromtimestamp(t).isoformat())

result = { "time": times, "snr": snrs, "isotime": isotimes, "latitude": latitude, "longitude": longitude}
json_string = json.dumps(result, indent=2)

print json_string

