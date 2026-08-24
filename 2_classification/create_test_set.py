# Create x,y test sets without running the ML algorithms
# This method was created to generate scaled Bull Point data so that a best model (.pkl file) can be applied to them.
# We need to create these data here and not through the usual train_test_split sklearn method, as the latter enforces a
# training and a test set. But given that here we want to apply the .pkl file to the whole dataset, we have this method that
# sets a single test set that contains the 100% of the scaled observations.
#This method eventually became useful not just for Bull Point, but for all other datasets that also needed to do drifting
# experiments.

import pandas as pd
import numpy as np
import io
import os
import csv
import fnmatch
import datetime

from sklearn.preprocessing import StandardScaler

path = './TH/' # Path where project files are located
input = 'drifted/1-min/' # Folder where input files (merged datasets) are located
results = 'drifted/x-y test sets/1-min/' # Folder where results are saved

seed = 100

def create_test_set():
  # Check if results folder exists, if not, create it
  if not os.path.exists(path + results):
    os.makedirs(path + results)

  X, y = [], [] # Complete features (X) and target/class (y) arrays
  X_test, y_test = [], [] # Separate complete arrays to train and test sets
  X_test_scaled = [] # Arrays to hold scaled values for certain ML algorithms

  filenames = [f for f in os.listdir(path + input) if fnmatch.fnmatch(f, '*.csv')]
  filenames = sorted(filenames)

  # For each dataset, do the following
  for f in filenames:
    print('======================== Dataset: ' + str(f) + '========================')
    dataset = f.split('.')

    # Check if dataset folder exists, if not, create it
    if not os.path.exists(path + results + dataset[0]):
      os.mkdir(path + results + dataset[0])

    # Phase 2 features
    # data = pd.read_csv(path + input + f, usecols = ['Sunangle', 'Temp2m', 'Dewpoint2m','Pressure', 'Precipitation', 'GHI', 'DHI', 'BNI', 'Value'])
    # Phase 3 features
    columns_to_exclude = ['Tagname', 'Date']
    data = pd.read_csv(path + input + f, usecols=lambda column: column not in columns_to_exclude)
    # data = pd.read_csv(path + input + f, usecols = ['Sunangle', 'Temp2m', 'Dewpoint2m',
                                                    # 'Pressure', 'Precipitation', 'GHI_N', 'DHI_N',
                                                    # 'BNI_N', 'zenith', 'elevation', 'equation_of_time', 'ghi_M', 'dhi_M', 'dni_M', 'Value'])
    X = data.copy(deep=True) # Features dataframe
    X = X[X.Value != 'Error'] # Some datasets had an Error class, which I remove
    X = X[X.Value != '0'] # Some datasets had an 0 class (similar to Error), which I remove
    X = X[X.Value != 0] # Some datasets had an 0 class (similar to Error), which I remove. In previous line I took 0 as string, here as integer, because both cases existed in the dataset
    y = X.pop('Value') # Target/class dataframe
    X_test = X
    y_test = y

    # Perform scaling
    # sc=StandardScaler()
    # scaler = sc.fit(X_test) # Because X_train is empty now, we fit to X_test
    # X_test_scaled = scaler.transform(X_test)
    X_test_scaled = X_test # some times no scaling performs better (especially with drifting analysis, so we also have this option; make sure to comment out the previous 3 lines that perform scaling!)

    np.savetxt(path + results + dataset[0] + '/X_test_scaled.csv', X_test_scaled, delimiter=",")
    # for the y dataset, I save them as dataframes, so that i also save the index of each target value
    y_test.to_csv(path + results + dataset[0] + '/y_test.csv', header=False)
create_test_set()
