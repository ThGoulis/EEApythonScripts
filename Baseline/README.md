Outliers Scripts
=
Prerequisites:
-
- Python 3.9
- Pandas 1.5.2
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
  
- Change the `countryCode = ["NL"]` with the code of country. You can also use the the array adove to exctract multiple countries.
- The script create a folder with the name of countryCode.
`working_directory = 'C:\path\to\directory\' + country + '\\'`
  
For functions.py:

- Change the name of `country = ['AT']` with the name of country how you add at main.py.

Input data
-
- Check the CsvToSQLDatabase folder

