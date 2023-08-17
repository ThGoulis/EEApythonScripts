For main.py:<br>
Import sqlite3, pandas, csv and functions libraries.

To run this script you need to create a sqlite database with the outputs files.

Create a folder for working_directory = "C:\path\to\directory\"<br>
Create a folder for Excel_directory = "C:\path\to\directory\"<br>
Specify the output folder final_Excel = "C:\path\to\directory\"<br>
Add the directory of the sqlite database at SqlDatabase = r"C:\path\to\database/database.sql"<br>
At variable 'countryCode' you need to change the value with the country code with one of adove to exctract the data from this country.<br>

Also you can change or leave it as it is the variable 'file' to generate the output file name.<br>
file = 'Outliers - ' + code<br>
extention = '.csv'

For functions.py:

Change the name of country = ['AT'] with the name of country how you add at main.py.<br>

<b>IMPORTANT NOTE:</b> you need to search and replace the ['AT'] with the name of country how want to exctract data. example: ['NL'], ['FR'] etc
