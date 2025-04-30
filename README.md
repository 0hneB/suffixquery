# SuffixQuery — KML Place Name Extractor

**SuffixQuery** is a standalone GUI tool for extracting place names from OpenStreetMap using the Overpass API. Choose a country, place types (`town`, `village`, etc.), and a suffix (like `ach`) to find matching names and export them as `.kml` files.

---

<details>
<summary>💡 Features</summary>

- Filter by place type: `village`, `town`, `city`, `hamlet`, `locality`, `farm`, `isolated_dwelling`  
- Auto-generates `.kml` files in the format `country__contain__position_term.kml`  
- Saves the file directly in the application folder  
</details>

<details>
<summary>🖥️ How to Use</summary>

1. Download and extract the application folder  
2. Select a country, match type, word position and place type   
3. Enter a term (e.g. `ach`)  
4. Click **Fetch Data**  
→ A file like `Germany__suffix__all_ach.kml` will appear in the folder you can select at `Select Output Dir`  
</details>

<details>
<summary>🗺️ Example Use Case</summary>

Want to find all towns and villages in **Germany** ending in `ach`?

→ Select `Germany`, type `ach`, choose `town` and `village`, check `suffix`, and hit **Fetch Data**  
→ You’ll get `Germany__suffix__all_ach.kml` with the results  
</details>

<details>
<summary>📄 License & Data Source</summary>

- Data from [OpenStreetMap](https://www.openstreetmap.org)  
- Usage follows the [ODbL license](https://opendatacommons.org/licenses/odbl/)  
- Queries use the [Overpass API](https://overpass-api.de/)  
</details>

<details>
<summary>👤 Credits & Contact</summary>

- Made by **BennoGHG**  
  > Discord: `benno2503`  
- Ideas & Testing: **AtomoMC**  
  > Discord: `atomomc3904`  
</details>

---

🔗 **GitHub Repository**  
[https://github.com/0hneB/suffixquery](https://github.com/0hneB/suffixquery)

