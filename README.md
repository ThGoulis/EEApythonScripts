# EEA Python Script for Data Extraction and Processing

[![GitHub license](https://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/nikoshet/spark-cherry-shuffle-service/master/LICENSE)

# Table of Contents

+ [About](#about)
+ [Getting Started](#getting_started)
    + [Prerequisites](#prerequisites)
    + [Convert Html files to Pdf](#converthtmltopdf)
+ [Input Data](#input_data)
+ [Execution Options](#execution_options)	
+ [Built With](#built_with)
+ [License](#license)

## About <a name = "about"></a>
The following scripts are created to extract and process data from the EEA Database. Their output is to be used by MS assessors during the reporting period. The scripts generate csv, html/pdf and excel files.  

## Getting Started <a name = "getting_started"></a>

The following instructions will help you to reproduce the same results. The scripts have been executed in windows. We have compared the extracted results and match with the results we get from the EEA Dashboard regarding Surface water bodies and Groundwater bodies. To complete the process you need to install the following packages.

# Prerequisites <a name = "prerequisites"></a>

As mentioned above, you will need to install the correct versions of Python, Python Pandas, Python csv, Python re, Python plot, wkhtmltopdf  libraries.
You need to download the Python version 3.9 via https://www.python.org/downloads/
also you need to install the following packages at your Pycharm IDE
```
pip install pandas
pip install csv
pip install plot
pip install re
```
For the wkhtmltopdf tool you need to download the following application from https://wkhtmltopdf.org/downloads.html

# Convert Html files to Pdf <a name  = "converthtmltopdf"></a>
You need to open the cmd terminal and run the following command in the directory where the html files have been created
```
    for %f in (.\*.html) do "c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" "%~nf.html" "%~nf.pdf"
```

# Input data <a name = "input_data"></a>
You need to download the following database version from Wise Water Framework Directive Database:
https://www.eea.europa.eu/en/datahub/datahubitem-view/dc1b1cdf-5fa0-4535-8c89-10cc051e00db
## Built With <a name = "built_with"></a>


# License <a name = "license"></a>
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.
