import netCDF4
import json
import datetime

#set manual number of radials and gates to read for now 
nradials = 50 
ngates = 10

dataset = netCDF4.Dataset("radar2.nc", "r")
dimensions = dataset.dimensions
variables = dataset.variables

time = variables["Time"]
snr = variables["SignalToNoiseRatio"]

times = []
isotimes = []
snrs = []

for r in range(0, nradials):
    beam = snr[r, 0:ngates].tolist()
    snrs.append(beam)
    t = time[r].tolist()
    times.append(t)
    isotimes.append(datetime.datetime.fromtimestamp(t).isoformat())
#f= open("test.txt", "w+")
f= open("test.js", "w+")
result = { "time": times, "snr": snrs, "isotime": isotimes}
json_string = json.dumps(result, indent=2)

f.write(json_string) 

# print json_string

