Baseline
=
Prerequisites:
-
- Python 3.9
- Python-csv 0.0.13
- Sqlite 3
```
pip install pandas
pip install python-csv
```
Execution instructions
-
For main.py:
- Import os, sqlite3, time, sqlite3, Error, function libraries
  
- To run this script you need to connect to the sqlite database.
  you specify the directory at:<br>
  `database = r"C:\path\to\directory/nameOfDatabase.sqlite"`
  
- Change the `countryCode = ["NL"]` with the code of country how you want to extract data.
- Specify the path of folder: `working_directory = 'C:\path\to\directory\' + country + '\\'` The countryCode will get the name of folder.
  
For functions.py:
- Need to install csv library to execute the fuctions.
  

Input data
-
- Find the database at: https://www.eea.europa.eu/data-and-maps/data/wise-wfd-4

