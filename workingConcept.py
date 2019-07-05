import warnings
warnings.simplefilter("ignore")
import os
import pyart
import matplotlib.pyplot
import matplotlib as mpl
import numpy as np
import gzip
import shutil
import xarray as xr
from funcs import read_casa_netcdf
import json
import pandas as pd
# import gyzip

grid_file = 'xmdl_grid.nc'
grid = pyart.io.grid_io.read_grid('xmdl_grid.nc')
dataset = xr.open_dataset(grid_file)
variables = list(dataset.variables)

lats = grid.point_latitude['data']
lons = grid.point_longitude['data']
zh = grid.fields['Reflectivity']['data']
# time = grid.variables['units']

latitude = []
longitude = []
reflectivity = []
times = []

# print(vars)
# print(grid.origin_longitude['data'][0])

latLonRefArray = np.stack([lats.ravel(), lons.ravel(), zh.ravel()], axis = 1)

# arrangedArray = pd.DataFrame(latLonRefArray, columns=['latitude', 'longitude', 'zh'])
# arrangedArray= arrangedArray.dropna()

# print(latLonRefArray)

# print(lats)
# print(lons)

# f= open("jsonVersionTest.json", "w+")
results = {"outputData": latLonRefArray.tolist()}
# json_string = json.dumps(results, indent=2)
# f.write(json_string)
with gzip.open("zipVersionTest.json", 'wb') as f:
    json_string = json.dumps(results, indent=2)
    f.write(json_string)


# arrangedArray.to_json('pandasFileTest.json', index=False, orient='table', double_precision=6)