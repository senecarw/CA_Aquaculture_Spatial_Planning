#Seneca and Sky Final Project - ENV 859 
#This script will pull data required for further analysis of Giant Kelp suitability based on EEZ boundaries, temperature, and depth conditions.

#1. Package Library
import arcpy
import numpy as np
import xarray as xr
from datetime import date, timedelta
import pandas as pd

##2. Import datasets
#Pull hexagon spatial analysis units from NOAA/ESRI


#Pull and clean temperature data from HYCOM and GFOS
"""
HYCOM GOFS 3.1 data pull (Python version)
Pulls water temperature for one depth layer, one region, one year,
and calculates the daily max and min temperature.

Install once:  pip install xarray netCDF4 pandas
"""
#Settings
#Select year
YEAR = 2022

# Select location: California coast bounding box for whole EEZ
LON_MIN, LON_MAX = 360 - 129, 360 - 117
LAT_MIN, LAT_MAX = 30.5, 42

#Selecting sea surface temperature
DEPTH_INDEX = 0

#Selecting time bounds
HOURS = [0, 3, 6, 9, 12, 15, 18, 21]

#Test URL
URL = ("https://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/"
       "data/hindcasts/{year}/hycom_glby_930_{date}12_t{hour:03d}_ts3z.nc")

#Make a list of days in year being selected
dates = pd.date_range(f"{YEAR}-01-01", f"{YEAR}-12-31")
print (dates)

#Pull US EEZ data from NOAA GeoPlatform

#Pull depth data from GEBCO

##3. Preliminary Analysis

#Loop through each day and 3hour hour time step in temperature data
daily_max = []   # one max grid per day
daily_min = []   # one min grid per day
good_dates = []  # days that loaded successfully

for date in dates:
    date_str = date.strftime("%Y%m%d")   # e.g. "20220115"
    temps = []                           # the 8 grids for this day

    for hour in HOURS:
        url = URL.format(year=YEAR, date=date_str, hour=hour)
        print(url)

        # Open the remote file (no download yet, just a pointer)
        try:
            ds = xr.open_dataset(url, decode_times=False)
        except Exception as e:
            print(f"Could not open {url}: {e}")
            continue   # skip this time step

        temp = (ds["water_temp"]
                .isel(time=0, depth=DEPTH_INDEX)
                .sel(lat=slice(LAT_MIN, LAT_MAX),
                     lon=slice(LON_MIN, LON_MAX))
                .load())

        temps.append(temp)
        ds.close()

# Collapse the day's grids to a single max and min grid
    if len(temps) == 0:
        print(f"No data for {date_str}, skipping.")
        continue

    day_stack = xr.concat(temps, dim="hour")        # stack the grids
    daily_max.append(day_stack.max(dim="hour"))     # warmest value per cell
    daily_min.append(day_stack.min(dim="hour"))     # coolest value per cell
    good_dates.append(date)

#Combine all days into one dataset with a "date" dimension
date_index = pd.Index(good_dates, name="date")
max_all = xr.concat(daily_max, dim=date_index)
min_all = xr.concat(daily_min, dim=date_index)

# Save results
max_all.to_netcdf(f"hycom_{YEAR}_max_daily.nc")
min_all.to_netcdf(f"hycom_{YEAR}_min_daily.nc")
print("Done!")