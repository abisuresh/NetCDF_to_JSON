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

grid_file = 'xmdl_grid.nc'
grid = pyart.io.grid_io.read_grid('xmdl_grid.nc')
dataset = xr.open_dataset(grid_file)
vars = list(dataset.variables)
print(vars)
print(grid.origin_longitude['data'][0])
