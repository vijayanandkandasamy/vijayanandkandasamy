#!/usr/bin/env python3

# Copyright 2016 Google Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


import csv
import requests
import io
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Classes to hold the data
class Covid19:
  def __init__(self, row):
    # Parse Covid 19 Data
    self.date = row[0]
    try:
      self.lat = float(row[12])
    except ValueError:
      self.lat = 0
    try:
      self.lon = float(row[13])
    except ValueError:
      self.lon = 0
    try:
      self.casecount = float(row[2])
    except ValueError:
      self.casecount = 0
    
def get_covid_data(url):

  Covid_Dataset_File = open('CovidStatsDec2020.csv')
  
  reader = csv.reader(Covid_Dataset_File)
  header = next(reader)
  cases = [Covid19(row) for row in reader]
  cases = [q for q in cases if q.casecount > 0]
  print (cases)
  return cases


# Control Marker Color And Size Based On Casecount
def get_marker(casecount):    
    if casecount < 10000:
      markersize = casecount * 0.06;
        return ('bo'), markersize
    if casecount < 25000:
      markersize = casecount * 0.006;
        return ('go'), markersize
    elif casecount < 50000:
      markersize = casecount * 0.006;
        return ('yo'), markersize
    else:
        markersize = casecount * 0.0006;
        return ('ro'), markersize


def create_png(url, outfile): 
  cases = get_covid_data('https://everywebworx.in/vijayanandkandasamy/bigdata/CovidCases_Dec2020.csv')
  print(cases[0].__dict__)

  # Set up Basemap
  mpl.rcParams['figure.figsize'] = '16, 12'
  m = Basemap(projection='kav7', lon_0=-90, resolution = 'l', area_thresh = 1000.0)
  m.drawcoastlines()
  m.drawcountries()
  m.drawmapboundary(fill_color='0.3')
  m.drawparallels(np.arange(-90.,99.,30.))
  junk = m.drawmeridians(np.arange(-180.,180.,60.))

  # Sort COVID Cases by casecount so that counts of smaller number are plotted after (i.e. on top of) larger ones and the larger ones have bigger circles, so we'll see both
  start_day = cases[-1].date
  end_day = cases[0].date
  cases.sort(key=lambda q: q.casecount, reverse=True)

  # Add COVID - 19 | Case Activity info to the plot
  for q in cases:
    x,y = m(q.lon, q.lat)
    mcolor, msize = get_marker(q.casecount)
    m.plot(x, y, mcolor, markersize=msize)

  # Add Chart Title
  plt.title("COVID 19 | Global Case Activity - Dec - 2020 | Data Analysis | Vijayanand Kandasamy")
  plt.savefig(outfile)

if __name__ == '__main__':
  url = 'https://everywebworx.in/vijayanandkandasamy/bigdata/CovidCases_Dec2020.csv'
  print (url)
  outfile = 'CovidStatsDec2020.png'
  create_png(url, outfile)
