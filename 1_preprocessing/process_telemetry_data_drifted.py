#!/usr/bin/python3

import os 
import sys 
import re
import ephem

import numpy as np
import pandas as pd

from pathlib import Path
from datetime import datetime

def get_comma_separated_args(option, opt, value, parser):
    """
        Splits the provided comma separated input into district values in a list.
    """
    setattr(parser.values, option.dest, value.split(','))


def calculate_sun_angle(lat, lon, date):
    obs = ephem.Observer()
    obs.lat = lat
    obs.long = lon
    obs.date = date
    sun = ephem.Sun(obs)
    sun.compute(obs)
    return float(sun.alt) * 57.2957795


def main():
    """
        The main function of the script where the input arguments are parsed and
        the serial port monitoring begins.
    """
    from optparse import OptionParser

    desc="""Use this tool to validate the AIVDM sentences received through a serial port."""
    parser = OptionParser(description=desc)
    parser.add_option("-i", "--input", type="string", dest="input", help="The input telemetry data Excel file", action='callback', callback=get_comma_separated_args)
    parser.add_option("-x", "--latitude", type="string", dest="latitude", help="The station location latitude")
    parser.add_option("-y", "--longitude", type="string", dest="longitude", help="The station location longitude")
    parser.add_option("-c", "--clean", action="store_true", dest="clean", help="Clean up the dataset values", default=False)

    # Parse the options
    (options, args) = parser.parse_args()

    # Validate arguments
    if not options.input:
        parser.error('No input file given')
    if not options.latitude:
        parser.error('No latitude given')
    if not options.longitude:
        parser.error('No longitude given')

    # Keep a reference to the CSV file names
    inputPartXslx = []
    inputPartCsvs = []

    # Open the individual input parts, cleanup and store as CSV
    for inputPart in options.input:
        inputPartXslx.append(os.path.join(sys.path[0], inputPart))
        inputPartCsvs.append(inputPartXslx[-1].replace('.xlsx', '.csv'))
        excel_telemetry_data_part = pd.read_excel(inputPartXslx[-1])
        excel_telemetry_data_part.to_csv(inputPartCsvs[-1], index=False)
    
    # Now combine the parts into one CSV
    combined_telemetry_csv_filename = re.sub('_Part\d', '.csv' if not options.clean else '_CL.csv', os.path.splitext(Path(inputPartCsvs[0]).name)[0]);
    combined_telemetry_csv = pd.concat([pd.read_csv(f) for f in inputPartCsvs ])
    combined_telemetry_csv=combined_telemetry_csv.drop(['PCUNAME'], axis=1)
    combined_telemetry_csv=combined_telemetry_csv.drop(['TIME_ORIG'], axis=1)
    combined_telemetry_csv=combined_telemetry_csv.drop(['Drift Minutes'], axis=1)
    # And sort everything
    combined_telemetry_csv = combined_telemetry_csv[(combined_telemetry_csv["TIME"] < '2022-01-01')]
    combined_telemetry_csv=combined_telemetry_csv.sort_values(by=['TIME'])

    # Drop the consecutive duplicate vales
    combined_telemetry_csv['PREVIOUS_VALUE'] = combined_telemetry_csv['VALUE'].shift(1)
    combined_telemetry_csv['NEXT_VALUE'] = combined_telemetry_csv['VALUE'].shift(-1)
    combined_telemetry_csv = combined_telemetry_csv.loc[combined_telemetry_csv['VALUE'] != combined_telemetry_csv['PREVIOUS_VALUE']]

    # Clean-up operation enabled
    if options.clean :
        # Remove occasional ON-OFFS
        combined_telemetry_csv['PREVIOUS_TIME'] = combined_telemetry_csv['TIME'].shift(1)
        combined_telemetry_csv['NEXT_TIME'] = combined_telemetry_csv['TIME'].shift(-1)
        combined_telemetry_csv['PREVIOUS_TIME_DIFF'] = combined_telemetry_csv.apply(
            lambda x: (datetime.fromisoformat(x['TIME']) - datetime.fromisoformat(x['PREVIOUS_TIME'])).seconds if isinstance(x['PREVIOUS_TIME'], str) else 9999, axis=1
        )
        combined_telemetry_csv['NEXT_TIME_DIFF'] = combined_telemetry_csv.apply(
            lambda x: (datetime.fromisoformat(x['NEXT_TIME']) - datetime.fromisoformat(x['TIME'])).seconds if isinstance(x['NEXT_TIME'], str) else 9999, axis=1
        )
        combined_telemetry_csv = combined_telemetry_csv.loc[
            (~ ((combined_telemetry_csv['VALUE'] == 'ON') & (combined_telemetry_csv['NEXT_VALUE'] == 'OFF') & (combined_telemetry_csv['NEXT_TIME_DIFF'] <= 1200))) & 
            (~ ((combined_telemetry_csv['VALUE'] == 'OFF') & (combined_telemetry_csv['PREVIOUS_VALUE'] == 'ON') & (combined_telemetry_csv['PREVIOUS_TIME_DIFF'] <= 1200))) 
        ]

        # Remove the added columns
        combined_telemetry_csv = combined_telemetry_csv.drop(['PREVIOUS_TIME'], axis=1)
        combined_telemetry_csv = combined_telemetry_csv.drop(['NEXT_TIME'], axis=1)
        combined_telemetry_csv = combined_telemetry_csv.drop(['PREVIOUS_TIME_DIFF'], axis=1)
        combined_telemetry_csv = combined_telemetry_csv.drop(['NEXT_TIME_DIFF'], axis=1)

    # # Remove the added columns
    # combined_telemetry_csv = combined_telemetry_csv.drop(['PREVIOUS_VALUE'], axis=1)
    # combined_telemetry_csv = combined_telemetry_csv.drop(['NEXT_VALUE'], axis=1)

    # Calculate the sunangle
    combined_telemetry_csv['SUNANGLE'] = combined_telemetry_csv.apply(
        lambda x: calculate_sun_angle(options.latitude, options.longitude, datetime.fromisoformat(x[1])), axis=1
    )
    sun_angle_col = combined_telemetry_csv.pop('SUNANGLE')
    combined_telemetry_csv.insert(2, 'SUNANGLE', sun_angle_col)

    # Output to a final CSV
    combined_telemetry_csv.to_csv(os.path.join(sys.path[0], combined_telemetry_csv_filename), index=False)

    # Finally remove the CSV parts
    for inputPartCsv in inputPartCsvs:
        os.remove(inputPartCsv)


if __name__ == '__main__':
    main()

