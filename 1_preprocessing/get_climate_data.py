import os
import shutil
import csv
import argparse
import cdsapi
import netCDF4
import glob 

import numpy as np
import pandas as pd

from pathlib import Path
from datetime import datetime
from netCDF4 import num2date

# Global variables
weather_data_file = 'weather_data.csv'
solar_insolation_data_file = 'solar_insolation_data.csv'

def download_weather_data(name, lat, lon, start, end):
    # Figure out the date range
    
    years = list(set(pd.date_range(start, end).strftime("%Y").tolist()))    
    months = list(set(pd.date_range(start, end).strftime("%m").tolist()))
    days = list(set(pd.date_range(start, end).strftime("%d").tolist()))
    years.sort()
    days.sort()
    months.sort()

    # Initialise the CDS API Client
    # Credentials are read from the environment so that no key is stored in the
    # repository. Set CDSAPI_URL / CDSAPI_KEY before running (see README).
    cdsapiClient = cdsapi.Client(
        url=os.environ.get('CDSAPI_URL', 'https://cds.climate.copernicus.eu/api/v2'),
        key=os.environ['CDSAPI_KEY']
    )

    for year in years:
        # Setup the yearly output directory
        output_dir = './{}/weather/{}'.format(name, year)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        file_location = os.path.join(output_dir, 'reanalysis-era5-land.nc')
        # And perform the CDS API Call
        cdsapiClient.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    '2m_dewpoint_temperature',
                    '2m_temperature',
                    'surface_pressure',
                    'total_precipitation',
                ],
                'year': [year],
                'month': months,
                'day': days,
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00',
                ],
                'area': [
                    lat, lon,
                    lat, lon
                ],
                'format': 'netcdf',
            },
            file_location)

        # Open netCDF4 file
        f = netCDF4.Dataset(file_location)

        # Extract variables
        t2m = f.variables['t2m']
        d2m = f.variables['d2m']
        sp = f.variables['sp']
        tp = f.variables['tp']

        # Get dimensions assuming 3D: time, latitude, longitude
        time_dim, lat_dim, lon_dim = t2m.get_dims()
        time_var = f.variables[time_dim.name]
        times = num2date(time_var[:], time_var.units)
        latitudes = f.variables[lat_dim.name][:]
        longitudes = f.variables[lon_dim.name][:]

        # =====================================================================
        # Write data as a table with columns including time, lat-lon etc....
        # =====================================================================
        filename = os.path.join(output_dir, weather_data_file)
        print(f'Writing data in tabular form to {filename} (this may take some time)...')
        times_grid, latitudes_grid, longitudes_grid = [
            x.flatten() for x in np.meshgrid(times, latitudes, longitudes, indexing='ij')]
        df = pd.DataFrame({
            'time': [t.isoformat() for t in times_grid],
            'latitude': latitudes_grid,
            'longitude': longitudes_grid,
            'Temp 2m': t2m[:].flatten() - 273.15,
            'Dewpoint 2m': d2m[:].flatten() - 273.15,
            'Pressure': sp[:].flatten(),
            'Precipitation': tp[:].flatten()})

        # Output to a new CSV
        df.to_csv(filename, index=False)
        
        # And now remove the downloaded NetCDF file
        os.remove(file_location)
        
    print('Downloading Weather Data Done')

def download_solar_insolation_data(name, lat, lon, start, end):
    # Initialise the CDS API Client
    # As above: the Atmosphere Data Store uses a separate account and key.
    cdsapiClient = cdsapi.Client(
        url=os.environ.get('ADSAPI_URL', 'https://ads.atmosphere.copernicus.eu/api/v2'),
        key=os.environ['ADSAPI_KEY']
    )

    # Setup the output directory
    output_dir = './{}/solar/'.format(name)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # And perform the CDS API Call
    file_location = os.path.join(output_dir, 'cams-solar-radiation-timeseries.nc')
    cdsapiClient.retrieve(
        'cams-solar-radiation-timeseries',
        {
            'sky_type': 'observed_cloud',
            'location': {
                'latitude': lat,
                'longitude':lon,
            },
            'altitude': '-999.',
            'date': f'{start}/{end}',
            'time_step': '15minute',
            'time_reference': 'universal_time',
            'format': 'netcdf',
        },
        file_location
    )
    
    # =====================================================================
    # Write data as a table with 4 columns: time, latitude, longitude, value
    # =====================================================================
    # Open netCDF4 file
    f = netCDF4.Dataset(file_location)

    # Extract variables
    time = f.variables['time']
    ghi = f.variables['GHI']
    dhi = f.variables['DHI']
    bni = f.variables['BNI']

    # Get dimensions assuming the existence of time
    times = num2date(time[:], time.units)

    filename = os.path.join(output_dir, solar_insolation_data_file)
    print(f'Writing data in tabular form to {filename} (this may take some time)...')
    times_grid, = [x.flatten() for x in np.meshgrid(times, indexing='ij')]
    df = pd.DataFrame({
        'time': [t.isoformat() for t in times_grid],
        'GHI': ghi[:].flatten(),
        'DHI': dhi[:].flatten(),
        'BNI': bni[:].flatten()})
    
    # Output to a new CSV
    df.to_csv(filename, index=False)
    print('Downloading Solar Insolation Data Done')

    # And now remove the downloaded CSV file
    os.remove(file_location)

def combine_data(name):
    # Combine the weather CSV files
    weather_filenames = [i for i in glob.glob('./{}/weather/*/{}'.format(name, weather_data_file))]
    combined_weather_csv = pd.concat([pd.read_csv(f) for f in weather_filenames ])
    combined_weather_csv.to_csv( "./{}/weather/{}".format(name, weather_data_file), index=False)

    # Now combine the weather and solar insolation data
    widfPd = pd.read_csv('./{}/weather/{}'.format(name, weather_data_file))
    sidfPd = pd.read_csv('./{}/solar/{}'.format(name, solar_insolation_data_file))
    combinedPd = pd.merge(widfPd, sidfPd, how='outer', on = 'time')
    combinedPd = combinedPd.sort_values(by=['time'])

    # Create a timestamp index and interpolate the missing weather values
    combinedPd['timestamp']=pd.to_datetime(combinedPd['time'])
    combinedPd.set_index(combinedPd['timestamp'], inplace=True)
    combinedPd['latitude'].ffill(inplace=True);
    combinedPd['longitude'].ffill(inplace=True);
    combinedPd['Temp 2m'].interpolate(method='time', inplace=True)
    combinedPd['Dewpoint 2m'].interpolate(method='time', inplace=True)
    combinedPd['Pressure'].interpolate(method='time', inplace=True)
    combinedPd['Precipitation'].interpolate(method='time', inplace=True)
    combinedPd.drop('timestamp', axis=1, inplace=True)

    # Output to a new CSV
    combinedPd.to_csv('./{}/{}.csv'.format(name, name), index=False)
    print('Combining Climate and Solar Data Done')

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

def main():
    """
        The main function of the script where the input arguments are parsed and
        the serial port monitoring begins.
    """
    from optparse import OptionParser

    desc="""Use this tool to validate the AIVDM sentences received through a serial port."""
    parser = OptionParser(description=desc)
    parser.add_option("--name", dest="name", help="The name of the output file")
    parser.add_option("--latitude", dest="lat", help="The station location latitude")
    parser.add_option("--longitude", dest="lon", help="The station location longitude")
    parser.add_option("--startDate", dest="start", help="The start date of the data - format YYYY-MM-DD")
    parser.add_option("--endDate", dest="end", help="The end date of the data - format YYYY-MM-DD")
    
    # Parse the options
    (options, args) = parser.parse_args()

    # Validate arguments
    if not options.name:
        parser.error('Name not given')
    if not options.lat:
        parser.error('Latitude not given')
    if not options.lon:
        parser.error('Longitude not given')
    if not valid_date(options.start):
        parser.error('Start date not given')
    if not valid_date(options.end):
        parser.error('End Date not given')

    # First, remove any previous files for this name
    namePath = './{}'.format(options.name)
    if os.path.exists(namePath) and os.path.isdir(namePath):
        shutil.rmtree(namePath)

    # Download the weather data
    download_weather_data(options.name, options.lat, options.lon, options.start, options.end)
    # Download the solar insolation data
    download_solar_insolation_data(options.name, options.lat, options.lon, options.start, options.end)
    # And combine everything in a single file
    combine_data(options.name)

if __name__ == '__main__':
    main()
