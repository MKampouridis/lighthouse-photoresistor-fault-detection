# Create merged datasets
# Merge datasets, but exclude one at a time. So if there are 7 NLB datasets, we merge 6, and leave the 7th out;
# then in the second iteration we merge a different set of 6 and leave a different 7th out, and so on. The process is similar
# to k-fold cross validation. We can then use these merged datasets for training and testing on the drifted data of the
# respective excluded (from merged) dataset.

import pandas as pd
import io
import os
import csv
import fnmatch
import datetime

path = './NLB/' # Path where project files are located
input = 'input-utc-cl/1-min/moving_averages/' # Folder where input files (merged datasets) are located
results = '../Merged datasets/NLB_merged/1-min/moving_averages/' # Folder where results are saved

# Check if results folder exists, if not, create it
if not os.path.exists(path + results):
  os.makedirs(path + results)

filenames = [f for f in os.listdir(path + input) if fnmatch.fnmatch(f, '*.csv')]
filenames = sorted(filenames)
fname_excluded = ''

for f in filenames:
  data = pd.DataFrame()
  print('======================== Dataset: ' + str(f) + '========================')
  for f2 in filenames:
    if (not f2.__eq__(f)):
      dataset = pd.read_csv(path + input + f2)

      data = pd.concat([data,dataset])
    else:
      fname_excluded = f2.split('.')[0]
  data.to_csv(path + results + 'nlb_merged_utc-cl-' + fname_excluded + '.csv', index=False)
