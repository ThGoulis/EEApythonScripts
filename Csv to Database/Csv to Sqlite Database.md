Csv to Sql Database for Outliers
=
Prerequest
-
- Csv
```
pip install python-csv
```
- Need to create only a sqlite database (not headers, data and data type) by following this tutorial:
  https://www.guru99.com/sqlite-database.html#2
    
Execution instructions:
=
For main.py:<br>
- Change the path of database: `conn = sqlite3.connect('C:/path/to/database/nameOfDatabase.sqlite')`<br>
- Change the path of Baseline Csv's files: `Baseline('C:/path/to/Baseline/csv/files', conn)`
- Change the path of Screening Csv's files: `Screening('C:/path/to/Screening/csv/files', conn)`
  
Input data:
=
- Use the extracted data from Baseline and Screening scripts.
