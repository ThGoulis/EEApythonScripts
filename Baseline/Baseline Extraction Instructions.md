# WISE Database Report Generator

This script extracts information from the WISE database and generates reports per country for MS assessors. It is designed to process data for various water body assessments, including surface and groundwater bodies, and produce detailed CSV reports.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [License](#license)
- [Contributing](#contributing)

## Features

- Connects to a WISE SQLite database.
- Extracts and processes data for specified country codes.
- Generates CSV reports in a structured directory format.
- Covers various aspects of water body assessments including chemical and ecological statuses.

## Requirements

- Python 3.6+
- SQLite3
- `argparse` module (standard in Python 3)
- `os` module (standard in Python 3)
- `time` module (standard in Python 3)
- Custom `function` module containing specific data extraction functions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ThGoulis/EEApythonScripts/Baseline
    ```
2. Navigate to the project directory:
    ```bash
    cd wise-database-report-generator
    ```
3. Ensure all required Python packages are installed (SQLite3 and standard libraries should be pre-installed with Python).

4. Ensure the `function` module is available and contains the necessary methods used in the script.

## Usage

The script is executed from the command line and requires three arguments:
- `db`: Path to the SQLite database file.
- `country`: Country code for which the report will be generated.
- `outputdir`: Directory where the CSV files will be saved. The path must not end with a backslash `\`.

### Command Line Arguments

```bash
python script.py <db> <country> <outputdir>
```

- `db`: Path to the SQLite database file.
country: Country code (e.g., 'DE' for Germany).
outputdir: Output directory for the CSV files.
### Example
bash
Copy code
python script.py data/wise_database.sqlite DE output/reports
This command connects to the wise_database.sqlite database, extracts information for Germany (DE), and saves the reports to the output/reports/DE directory.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing
Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

### Explanation of the `README.md` Sections:

- **Features**: Lists the key functionalities of the script.
- **Requirements**: Specifies the Python version and modules needed to run the script.
- **Installation**: Instructions for cloning the repository and setting up the environment.
- **Usage**: Explains how to use the script, including the command line arguments.
- **Example**: Provides an example command to run the script.
- **License**: Mentions the project's licensing (replace with actual license used).
- **Contributing**: Encourages contributions and explains how to do so.

Feel free to add more details or modify the instructions as needed based on your project's specifics and your target audience.
