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
from osgeo import gdal 
from osgeo import ogr 
from osgeo import osr 
from osgeo import gdalnumeric 
from osgeo import gdalconst 
from PIL import Image
# import gyzip

#import gridded netcdf data from a file
grid_file = 'xmdl_grid.nc'

#read netcdf data
grid = pyart.io.grid_io.read_grid('xmdl_grid.nc')

#open dataset within gridded file
dataset = xr.open_dataset(grid_file)

#set the list of all the variables in the dataset to another variable
variables = list(dataset.variables)

#get the longitude, latitude and horizontal reflectivity of the data into variables
lats = grid.point_latitude['data']
lons = grid.point_longitude['data']
zh = grid.fields['Reflectivity']['data']
# time = grid.variables['units']

#create empty arrays for holding the latitude, longitude, reflectivity and timestamp data
latitude = []
longitude = []
reflectivity = []
times = []

# print(variables)
# print(grid.origin_longitude['data'][0])

#Create an array with all of the data in a stacked format compatible with converting to JSON
latLonRefArray = np.stack([lats.ravel(), lons.ravel(), zh.ravel()], axis = 1)

# arrangedArray = pd.DataFrame(latLonRefArray, columns=['latitude', 'longitude', 'zh'])
# arrangedArray= arrangedArray.dropna()

# print(latLonRefArray)

# print(lats)
# print(lons)
#


# f = open("jsonVersionTest.json", "w+")

#create an object of all of the data and save it to a variable called results
results = {"outputData": latLonRefArray.tolist()}

#format the data with indentation
json_string = json.dumps(results, indent=2)

#encode the json string into utf-8 format
json_bytes = json_string.encode('utf-8')

# json_string = json.dumps(results, indent=2)
# f.write(json_string)
# with gzip.open("outputTest.json", 'w+') as fout:
#     # json_string = json.dumps(results, indent=2)
#     fout.write(json_string)

#write the resulting JSON to a zipped file
with gzip.GzipFile("nextTest.json.gz", 'w') as fout:
    fout.write(json_bytes)


#convert gridded file to geoTIFF format (black and white)
os.system("gdal_translate -of GTiff " + "netCDF:xmdl_grid.nc" + ":Reflectivity xmdl_grid_test.tif")

#convert black and white tiff image to color 
os.system("gdaldem color-relief " + "xmdl_grid_test.tif " + "color_table.csv " + "xmdl_grid_colors_test.tif" )

#convert color tiff image to jpeg 

#ATTEMPT 1 to convert to jpg
# newImage = Image.open("xmdl_grid_test.tif")
# newImage.mode = 'I'
# newImage.point(lambda i:i*(1./256)).convert('L').save('new.jpeg')

#ATTEMPT 2 
# mypath = os.getcwd()
# for root, dirs, files in os.walk(mypath, topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
#         if os.path.splitext(os.path.join(root, name))[1].lower() == 'xmdl_grid_colors.tiff':
#             if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
#                 print("JPG already exists" %name)
#             else:
#                 outfile = os.path.splitext(os.path.join(root, name))[0] + "new.jpg"
#                 try:
#                     im = Image.open(os.path.join(root, name))
#                     print("Generating jpg")
#                     im.thumbnail(im.size)
#                     im.save(outfile, "JPEG", quality=100)
#                 except Exception as e:
#                     print(e)

#ATTEMPT3 
# infile = 'xmdl_grid.tif'
# for 'infile' in os.listdir("./"):
#     print ("file : ") 
#     print(infile)
#     if infile[-3:] == "tif" or infile[-3:] == "bmp" :
#         outfile = infile[:-3] + "jpeg"
#         im = Image.open(infile)
#         print("new filename is:") 
#         print(outfile)
#         out = im.convert("RGB")
#         out.save(outfile, "JPEG", quality=90)



# arrangedArray.to_json('pandasFileTest.json', index=False, orient='table', double_precision=6)
