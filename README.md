# SuffixQuery - KML Place Name Extractor

**SuffixQuery** is a standalone GUI tool for extracting place names from OpenStreetMap via the Overpass API. Specify a country, place types (e.g. town, village, city), and a suffix (e.g. `ach`) to fetch all matching names and export them as a `.kml` file.

<details>
<summary>💡 Features</summary>

- ✅ Filter by place type (village, town, city, road)  
- ✅ Export `.kml` files as `country--suffix.kml`  
- ✅ Files are saved automatically to the application folder  
</details>

<details>
<summary>🖥️ How to Use</summary>

1. Download and extract the application folder.  
2. Select a country, enter a suffix (e.g. `ach`), choose place types, and click **Fetch Data**.  
3. The KML file will be saved in the same folder as `country--suffix.kml`.  
</details>

<details>
<summary>🗺️ Example Use Case</summary>

Want all towns and villages in Germany ending in `ach`?  

→ Choose **Germany**, type `ach`, select **town** and **village**, check **suffix**, and click **Fetch Data**.  
→ You’ll get `germany--ach.kml` with all matching results.  
</details>

<details>
<summary>🔒 License & Attribution</summary>

- Data provided by [OpenStreetMap](https://www.openstreetmap.org) under the [ODbL license](https://opendatacommons.org/licenses/odbl/).  
- Queries are powered by the [Overpass API](https://overpass-api.de/).  
</details>

<details>
<summary>🧑‍💻 Credits</summary>

- Made by **BennoGHG**  
- Testing & Ideas: **AtomoMC**  
</details>

---

🌐 **GitHub Repository**  
[https://github.com/0hneB/suffixquery](https://github.com/0hneB/suffixquery)
