#!/bin/bash

sudo apt-get install wget

# Remove older copy of file, if it exists
rm -f CovidStatsDec2020.csv

# Download latest data from Repository
wget https://everywebworx.in/vijayanandkandasamy/bigdata/CovidCases_Dec2020.csv -O CovidStatsDec2020.csv

