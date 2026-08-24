## To capture the temporal effects of the existing features on the sensor light, I'm creating moving averages of all features. I'm using a window of 2 steps, which will allow to focus on On/Off pairs and observe how their values are affected over time.
## Because we have different types of files for the NLB and TH (including drifted and merged), I need to run this method for each of the above types. Essentially, I need to put in the input folder all relevant files that I want to add the new features, and then these are going to be created in the results folder.
## This only needs to happen once - after I've created those files, I can use them as input files for drifting analysis etc.

import pandas as pd
import io
import os
import csv
import fnmatch
import datetime

path = './TH/'
input = 'drifted/1-min/'
results = 'drifted/1-min/moving_averages/' # Folder where results are saved
filenames = [f for f in os.listdir(path + input) if fnmatch.fnmatch(f, '*.csv')]
filenames = sorted(filenames)
names = []

for f in filenames:
  data = pd.DataFrame()
  print('======================== Dataset: ' + str(f) + '========================')
  names.append(f)
  df = pd.read_csv(path + input + f, sep='\,') # Change this to the path of your csv file.

  # Removing Date, Value, Tagname, as I don't want to calculate new features (e.g. moving average) for them
  X = df.drop(['Date', 'Value', 'Tagname'], axis=1)

  temp = pd.DataFrame()
  for col_name in X.columns:
    temp[col_name + '_MA'] = X[col_name].rolling(window=2, min_periods=1).mean() # rolling window of 2. Given that there's always alternate states (on/off), it might be useful to have a rolling window of the features' values to see if we can capture how changes in weather conditions affect the sensor's state transitions.
    # I also considered using ratios (next two lines below), but they resulted to a high number of NaN, and as a result I discarded this approach of generating new features.
    #X[col_name + '_ratio'] = X[col_name].pct_change()
    #X[col_name + '_lagged'] = X[col_name] * X['Lagged_values']

  # Concatenate the original (df) dataframe with the newly created temp, which holds the new features. Place them before the last column of df, to ensure that Value (On/Off) remains the last column.
  result = pd.concat([df.iloc[:, :-1], temp, df.iloc[:, -1:]], axis=1)
  result
  result.to_csv(path + results + f, index=False)
