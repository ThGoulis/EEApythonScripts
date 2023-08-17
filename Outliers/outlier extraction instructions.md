Prerequisites:
- Python 3.9
- Pandas 1.5.2
- Python-csv 0.0.13
```
pip install pandas
pip install python-csv
```
Execution instructions:

For main.py:<br>
- Import sqlite3, pandas, csv and functions libraries.

- To run this script you need to create a sqlite database with the outputs files.

- Create/Specify a folder for Excel_directory = "C:\path\to\directory\"<br>
- Create/Specify the output folder final_Excel = "C:\path\to\directory\"<br>
- Add the directory of the sqlite database at SqlDatabase = r"C:\path\to\database/database.sql"<br>
- At variable 'countryCode' you need to change the value with the country code with one of adove to exctract the data from this country.<br>

- Also you can change or leave it as it is the variable 'file' to generate the output file name.<br>
file = 'Outliers - ' + code<br>
extention = '.csv'

For functions.py:

- Change the name of country = ['AT'] with the name of country how you add at main.py.

Input data:
- Check the CsvToSQLDatabase folder
