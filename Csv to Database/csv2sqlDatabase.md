Csv to Sql Database
=
Prerequest
- Csv

  
import csv
import sqlite3
import glob
import os


    conn = sqlite3.connect('C:/Users/Theofilos Goulis/PycharmProjects/Outliers/BaselineScreeningOutliers.sqlite')
    do_directory('C:/Users/Theofilos Goulis/Documents/ScreeningAT/3rdReportCsvAT', conn)
