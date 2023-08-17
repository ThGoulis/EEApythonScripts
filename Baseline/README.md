For main.py:

- To run this script you need to connect to the sqlite database.
  you specify the directory at:
  database = r"C:\path\to\directory/nameOfDatabase.sqlite"
  
- Import sqlite3, time, csv, os and functions libraries.
- Change the countryCode = ["NL"] with the code of country.
- The script create a folder with the name of countryCode.
  
  You can also use the the array adove to exctract multiple countries.
- working_directory = 'C:\path\to\directory\' + country + '\\'

At variable 'countryCode' you need to change the value with the country code with one of adove to exctract the data from this country.

Also you can change or leave it as it is the variable 'file' to generate the output file name.
file = 'Outliers - ' + code
extention = '.csv'

For functions.py:

Change the name of country = ['AT'] with the name of country how you add at main.py
