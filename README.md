# SuffixQuery - KML Place Name Extractor

SuffixQuery is a Python-based GUI tool that allows users to extract place names from OpenStreetMap data using the Overpass API. Users can specify a country, place types (like town, city, village), and a suffix (e.g. "ach") to find all matching locations and export them to a `.kml` file for use in mapping applications.

---

## 💡 Features

- ✅ Allows filtering by place type (village, town, city, road)
- ✅ Generates `.kml` files in the format `country--suffix.kml`
- ✅ Automatically saves the KML file in the script's directory

---

## 🖥️ How to Use

1. Make sure you have Python 3 installed.
2. Clone this repo or download the source files.
3. Create a .bat file and run it or just double click the .py file
4. Select a country, enter a suffix (e.g. `ach`), choose place types, and click **Fetch Data**.
5. The KML file will be saved in the same folder.
---

## 🗺️ Example Use Case

Want to find all towns and villages in Germany ending in **"ach"**?  
→ Just choose "Germany", enter `"ach"`, select "town" and "village", and hit **Fetch Data**.  
You'll get `germany--ach.kml` with matching places.

---

## 📁 Output

- Saved in the same folder as the script.
- Filename format: `country--suffix.kml` (e.g., `austria--dorf.kml`)

---

## 🔒 License & Attribution
 
 data is provided by **OpenStreetMap**, and usage must comply with the [ODbL license](https://opendatacommons.org/licenses/odbl/).
 Data provided by the **Overpass API**, © OpenStreetMap contributors (ODbL).

## 🧑‍💻 Credits

Made by **BennoGHG**

## 🌐 GitHub Repo

https://github.com/0hneB/suffixquery
