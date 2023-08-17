Csv to Sql Database
=
Prerequest
-
- Csv
```
pip install python-csv
```
- Need to create only a sqlite database (not headers) by following this tutorial:
  https://www.guru99.com/sqlite-database.html#2

For main.py:<br>
- Import sqlite3, glob, csv and os libraries.
- Change the `conn = sqlite3.connect('C:/path/to/database/.sqlite')`
`do_directory('C:/Users/Theofilos Goulis/Documents/ScreeningAT/3rdReportCsvAT', conn)`

Input data:
-
- Check the CsvToSQLDatabase folder
