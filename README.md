# Suffix Query Tool

A simple Python script that allows users to fetch place names with specific suffixes from different countries using the Overpass API. The results are saved in a KML format, ready to be used in mapping applications like Google Earth.

## Features

- Select a country from a dropdown list.
- Specify a suffix (e.g., "ach", "ton").
- Filter results by place types such as village, town, or city.
- Fetch data from the Overpass API and save it as a KML file.
- Automatically save the KML file with a filename formatted as `country--suffix.kml`.
- Cross-platform support for both Windows and macOS.

## Installation

### Prerequisites

Before running the script, you need to install the required Python dependencies.

1. **Python 3.x**: Make sure you have Python 3 installed. You can download it from the official website: [https://www.python.org/](https://www.python.org/).
   
2. **Install required dependencies**:  
   The script uses the `requests` library to fetch data from the Overpass API. If it's not already installed, you can install it using pip:
   ```bash
   pip install requests
