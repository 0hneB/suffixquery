import subprocess
import sys
import requests
import tkinter as tk
from tkinter import ttk, filedialog
import xml.etree.ElementTree as ET
import os
import threading
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def resource_path(relative_path):
    """ Get absolute path to resource (for dev and for PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Auto-install
def install_requirements():
    packages = ["requests"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
install_requirements()

# Words to ignore
ignore_words = [
    "le", "la", "les", "l'", "du", "des", "de", "la", "saint", "sainte", "saintes", 
    "sur", "en", "aux", "mont", "et", "ou", "par", "et", "de", "Saint", "Sainte", "La", "Les", "Le"
]

# Country QIDs
country_qids = {
    "Afghanistan": "Q889",
    "Albania": "Q222",
    "Algeria": "Q262",
    "Andorra": "Q228",
    "Angola": "Q916",
    "Antigua and Barbuda": "Q781",
    "Argentina": "Q414",
    "Armenia": "Q399",
    "Australia": "Q408",
    "Austria": "Q40",
    "Azerbaijan": "Q227",
    "Bahamas": "Q778",
    "Bahrain": "Q398",
    "Bangladesh": "Q902",
    "Barbados": "Q244",
    "Belarus": "Q184",
    "Belgium": "Q31",
    "Belize": "Q242",
    "Benin": "Q962",
    "Bhutan": "Q917",
    "Bolivia": "Q750",
    "Bosnia and Herzegovina": "Q225",
    "Botswana": "Q963",
    "Brazil": "Q155",
    "Brunei": "Q921",
    "Bulgaria": "Q219",
    "Burkina Faso": "Q965",
    "Burundi": "Q967",
    "Cambodia": "Q424",
    "Cameroon": "Q1009",
    "Canada": "Q16",
    "Cape Verde": "Q1011",
    "Central African Republic": "Q929",
    "Chad": "Q657",
    "Chile": "Q298",
    "China": "Q148",
    "Colombia": "Q739",
    "Comoros": "Q970",
    "Congo (Brazzaville)": "Q971",
    "Congo (Kinshasa)": "Q974",
    "Costa Rica": "Q800",
    "Croatia": "Q224",
    "Cuba": "Q241",
    "Cyprus": "Q229",
    "Czech Republic": "Q213",
    "Denmark": "Q35",
    "Djibouti": "Q977",
    "Dominica": "Q784",
    "Dominican Republic": "Q786",
    "East Timor": "Q574",
    "Ecuador": "Q736",
    "Egypt": "Q79",
    "El Salvador": "Q792",
    "Equatorial Guinea": "Q983",
    "Eritrea": "Q986",
    "Estonia": "Q191",
    "Eswatini": "Q1050",
    "Ethiopia": "Q115",
    "Fiji": "Q712",
    "Finland": "Q33",
    "France": "Q142",
    "Gabon": "Q1000",
    "Gambia": "Q1005",
    "Georgia": "Q230",
    "Germany": "Q183",
    "Ghana": "Q117",
    "Greece": "Q41",
    "Grenada": "Q769",
    "Guatemala": "Q774",
    "Guinea": "Q1006",
    "Guinea-Bissau": "Q1007",
    "Guyana": "Q734",
    "Haiti": "Q790",
    "Honduras": "Q783",
    "Hungary": "Q28",
    "Iceland": "Q189",
    "India": "Q668",
    "Indonesia": "Q252",
    "Iran": "Q794",
    "Iraq": "Q796",
    "Ireland": "Q27",
    "Israel": "Q801",
    "Italy": "Q38",
    "Ivory Coast": "Q1008",
    "Jamaica": "Q766",
    "Japan": "Q17",
    "Jordan": "Q810",
    "Kazakhstan": "Q232",
    "Kenya": "Q114",
    "Kiribati": "Q710",
    "Kuwait": "Q817",
    "Kyrgyzstan": "Q813",
    "Laos": "Q819",
    "Latvia": "Q211",
    "Lebanon": "Q822",
    "Lesotho": "Q1013",
    "Liberia": "Q1014",
    "Libya": "Q1016",
    "Liechtenstein": "Q347",
    "Lithuania": "Q37",
    "Luxembourg": "Q32",
    "Madagascar": "Q1019",
    "Malawi": "Q1020",
    "Malaysia": "Q833",
    "Maldives": "Q826",
    "Mali": "Q912",
    "Malta": "Q233",
    "Marshall Islands": "Q709",
    "Mauritania": "Q1025",
    "Mauritius": "Q1027",
    "Mexico": "Q96",
    "Micronesia": "Q702",
    "Moldova": "Q217",
    "Monaco": "Q235",
    "Mongolia": "Q711",
    "Montenegro": "Q236",
    "Morocco": "Q1028",
    "Mozambique": "Q1029",
    "Myanmar": "Q836",
    "Namibia": "Q1030",
    "Nauru": "Q697",
    "Nepal": "Q837",
    "Netherlands": "Q55",
    "New Zealand": "Q664",
    "Nicaragua": "Q811",
    "Niger": "Q1032",
    "Nigeria": "Q1033",
    "North Korea": "Q423",
    "North Macedonia": "Q221",
    "Norway": "Q20",
    "Oman": "Q842",
    "Pakistan": "Q843",
    "Palau": "Q695",
    "Panama": "Q804",
    "Papua New Guinea": "Q691",
    "Paraguay": "Q733",
    "Peru": "Q419",
    "Philippines": "Q928",
    "Poland": "Q36",
    "Portugal": "Q45",
    "Qatar": "Q846",
    "Romania": "Q218",
    "Russia": "Q159",
    "Rwanda": "Q1037",
    "Saint Kitts and Nevis": "Q763",
    "Saint Lucia": "Q760",
    "Saint Vincent and the Grenadines": "Q757",
    "Samoa": "Q683",
    "San Marino": "Q238",
    "Sao Tome and Principe": "Q1039",
    "Saudi Arabia": "Q851",
    "Senegal": "Q1041",
    "Serbia": "Q403",
    "Seychelles": "Q1042",
    "Sierra Leone": "Q1044",
    "Singapore": "Q334",
    "Slovakia": "Q214",
    "Slovenia": "Q215",
    "Solomon Islands": "Q685",
    "Somalia": "Q1045",
    "South Africa": "Q258",
    "South Korea": "Q884",
    "South Sudan": "Q958",
    "Spain": "Q29",
    "Sri Lanka": "Q854",
    "Sudan": "Q1049",
    "Suriname": "Q730",
    "Sweden": "Q34",
    "Switzerland": "Q39",
    "Syria": "Q858",
    "Tajikistan": "Q863",
    "Tanzania": "Q924",
    "Thailand": "Q869",
    "Togo": "Q945",
    "Tonga": "Q678",
    "Trinidad and Tobago": "Q754",
    "Tunisia": "Q948",
    "Turkey": "Q43",
    "Turkmenistan": "Q874",
    "Tuvalu": "Q672",
    "Uganda": "Q1036",
    "Ukraine": "Q212",
    "United Arab Emirates": "Q878",
    "United Kingdom": "Q145",
    "United States": "Q30",
    "Uruguay": "Q77",
    "Uzbekistan": "Q265",
    "Vanuatu": "Q686",
    "Vatican City": "Q237",
    "Venezuela": "Q717",
    "Vietnam": "Q881",
    "Yemen": "Q805",
    "Zambia": "Q953",
    "Zimbabwe": "Q954"
}

def generate_query(country, match_terms, place_types):
    qid = country_qids.get(country)
    if not qid:
        return None
    place_filter = "|".join(place_types).replace(",", "|").replace(", ", "|")
    match_regex = '|'.join(match_terms)
    query = f"""
    [out:json][timeout:1000];
    area["wikidata"="{qid}"]->.searchArea;
    (
      node["place"~"^{place_filter}$"]["name"~"{match_regex}"](area.searchArea);
    );
    out;
    """
    return query

def save_to_kml(data, country, match_terms, match_type):
    try:
        # Create KML directory if it doesn't exist
        kml_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kml_output")
        update_status(f"Creating output directory...", "#FFA500")
        os.makedirs(kml_dir, exist_ok=True)
        
        update_status(f"Generating KML structure for {len(data.get('elements', []))} places...", "#FFA500")
        kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(kml, "Document")
        
        # Add description with query information
        desc = ET.SubElement(document, "description")
        desc.text = f"Country: {country}, Match Type: {match_type}, Terms: {','.join(match_terms)}"
        
        # Add a simple style
        style = ET.SubElement(document, "Style", id="placemarkStyle")
        icon_style = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon_style, "scale").text = "1.0"
        ET.SubElement(ET.SubElement(icon_style, "Icon"), "href").text = "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"
        
        # Count for found places
        count = 0
        
        update_status(f"Adding place details to KML...", "#FFA500")
        for element in data.get("elements", []):
            if element["type"] == "node":
                name = element["tags"].get("name", "Unknown")
                lat = element["lat"]
                lon = element["lon"]
                
                placemark = ET.SubElement(document, "Placemark")
                ET.SubElement(placemark, "name").text = name
                ET.SubElement(placemark, "styleUrl").text = "#placemarkStyle"
                
                # Add description with place type
                place_type = element["tags"].get("place", "Unknown type")
                desc = ET.SubElement(placemark, "description")
                desc.text = f"Type: {place_type}"
                
                point = ET.SubElement(placemark, "Point")
                ET.SubElement(point, "coordinates").text = f"{lon},{lat}"
                count += 1

        country_safe = country.replace(" ", "_").capitalize()
        terms_safe = "_".join(match_terms).replace("|", "_").replace('^', '').replace('(', '').replace(')', '').replace('$', '')
        positions = "-".join([k.replace(" ", "") for k, v in word_positions.items() if v.get()]) or "all"
        filename = f"{country_safe}__{match_type}__{positions}__{terms_safe}.kml"
        kml_path = os.path.join(kml_dir, filename)

        # Convert XML to string and write to file
        update_status(f"Writing KML file to disk...", "#FFA500")
        tree = ET.ElementTree(kml)
        tree.write(kml_path, encoding="utf-8", xml_declaration=True)

        update_status(f"Saved {count} places to {filename}", "green")
        
        # Open the KML directory
        if count > 0 and open_folder_var.get():
            update_status(f"Opening output folder...", "green")
            os.startfile(kml_dir)
            
    except Exception as e:
        update_status(f"Save error: {e}", "red")

def fetch_data_thread():
    country = country_combobox.get()
    raw_input = suffix_entry.get().strip()
    place_types = [pt for pt in place_types_checkbuttons if place_types_checkbuttons[pt].get()]
    match_type = match_type_var.get()

    if not country or not raw_input or not place_types:
        update_status("Please fill out all fields", "red")
        return

    # Process the input terms - CHANGED from pipe to comma separator
    terms = raw_input.split(",")
    terms = [term.strip() for term in terms]  # Clean up whitespace
    
    # Handle ignored words based on the user's choice
    if ignore_check_var.get():
        terms = [term for term in terms if term.lower() not in ignore_words]

    # Handle double-barrel names (like Laragne-Montéglin -> Laragne Montéglin)
    terms = [t.replace("-", " ") if "-" in t else t for t in terms]

    # Word position filtering
    selected_positions = [key for key, var in word_positions.items() if var.get()]

    def match_word_position(term, match_type):
        regex_parts = []
        
        # Ignore unwanted words (like articles, common prefixes)
        terms_to_match = [word for word in term.split() if word.lower() not in ignore_words]
        cleaned_term = " ".join(terms_to_match)

        for pos in selected_positions:
            if pos == "First Word":
                if match_type == "prefix":
                    regex_parts.append(rf"^{cleaned_term}")
                elif match_type == "suffix":
                    regex_parts.append(rf"^{cleaned_term}(\b|$)")
                elif match_type == "contains":
                    regex_parts.append(rf"^{cleaned_term}$|^{cleaned_term}\b")
            elif pos == "Second Word":
                regex_parts.append(rf"\b\w+\s{cleaned_term}")
            elif pos == "Third Word":
                regex_parts.append(rf"\b\w+\s\w+\s{cleaned_term}")
            elif pos == "Last Word":
                regex_parts.append(rf"{cleaned_term}$")

        return "|".join(regex_parts) if regex_parts else cleaned_term

    # Apply word-position-aware regex transformation
    if selected_positions:
        terms = [match_word_position(t, match_type) for t in terms]
    else:
        if match_type == "prefix":
            terms = [f"^{t}" for t in terms]
        elif match_type == "suffix":
            terms = [f"{t}$" for t in terms]

    query = generate_query(country, terms, place_types)
    if not query:
        update_status("Invalid country", "red")
        return

    update_status(f"Preparing query for {country}...", "#FFA500")  # Orange for working

    try:
        # Show the query in the console for debugging
        print(f"Sending query: {query}")
        
        update_status(f"Calling Overpass API for {country}... This may take a moment.", "#FFA500")
        response = requests.get("https://overpass-api.de/api/interpreter", params={"data": query})
        if response.status_code != 200:
            raise Exception(f"API returned status code {response.status_code}")

        update_status(f"Processing results from Overpass API...", "#FFA500")
        data = response.json()

        if len(data["elements"]) > 0:
            update_status(f"Found {len(data['elements'])} places. Creating KML file...", "#FFA500")
            save_to_kml(data, country, terms, match_type)
        else:
            update_status(f"No matching data found for '{raw_input}' in {country}", "red")
    except Exception as e:
        update_status(f"API error: {e}", "red")

def update_status(message, color):
    status_label.config(text=message, fg=color)

def select_output_dir():
    directory = filedialog.askdirectory(title="Select Output Directory for KML Files")
    if directory:
        global kml_dir
        kml_dir = directory
        update_status(f"Output directory set to: {directory}", "green")

# UI
root = tk.Tk()
root.title("Overpass Tool by BennoGHG")
root.geometry("1000x800")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=8, background="#2a2a2a", foreground="white", borderwidth=0)
style.map("TButton", background=[("active", "#3498db")])

# Main container with padding
main_frame = tk.Frame(root, bg="#1e1e1e", padx=20, pady=10)
main_frame.pack(fill="both", expand=True)

# Country selection
tk.Label(main_frame, text="Select Country:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(anchor="w")
def on_country_entry(event):
    typed = country_combobox.get().lower()
    filtered = [c for c in country_qids if typed in c.lower()]
    country_combobox['values'] = filtered
    # Prevent losing focus after typing
    country_combobox.icursor('end')  # Move cursor to end
    root.after(50, lambda: country_combobox.focus_set())  # Keep focus

country_combobox = ttk.Combobox(main_frame, values=sorted(country_qids.keys()), font=("Segoe UI", 12))
country_combobox.pack(pady=(0, 10), fill="x")
country_combobox.bind('<KeyRelease>', on_country_entry)

# Terms input - CHANGED instruction text
tk.Label(main_frame, text="Enter Terms (comma separated, e.g. 'ach,by,ville'):", font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(anchor="w")
suffix_entry = tk.Entry(main_frame, font=("Segoe UI", 12))
suffix_entry.pack(pady=(0, 10), fill="x")

# Match Type
match_frame = tk.LabelFrame(main_frame, text="Match Type", font=("Segoe UI", 12), bg="#1e1e1e", fg="white", padx=10, pady=5)
match_frame.pack(fill="x", pady=(0, 10))

match_type_var = tk.StringVar(value="suffix")
for opt in ["prefix", "suffix", "contains"]:
    tk.Radiobutton(match_frame, text=opt.capitalize(), variable=match_type_var, value=opt,
                   font=("Segoe UI", 12), bg="#1e1e1e", fg="white", selectcolor="#34495e").pack(side="left", padx=10)

# Word Positions
position_frame = tk.LabelFrame(main_frame, text="Word Position(s)", font=("Segoe UI", 12), bg="#1e1e1e", fg="white", padx=10, pady=5)
position_frame.pack(fill="x", pady=(0, 10))

word_positions = {
    "First Word": tk.BooleanVar(),
    "Second Word": tk.BooleanVar(),
    "Third Word": tk.BooleanVar(),
    "Last Word": tk.BooleanVar()
}

for label in word_positions:
    tk.Checkbutton(position_frame, text=label, variable=word_positions[label],
                   font=("Segoe UI", 10), bg="#1e1e1e", fg="white",
                   selectcolor="#34495e").pack(side="left", padx=10)

# Options Frame
options_frame = tk.LabelFrame(main_frame, text="Options", font=("Segoe UI", 12), bg="#1e1e1e", fg="white", padx=10, pady=5)
options_frame.pack(fill="x", pady=(0, 10))

ignore_check_var = tk.BooleanVar(value=True)  # Default value: checked (True)
tk.Checkbutton(options_frame, text="Ignore common words (e.g. 'Le', 'La', 'Saint')", variable=ignore_check_var,
               font=("Segoe UI", 12), bg="#1e1e1e", fg="white", selectcolor="#34495e").pack(anchor="w")

open_folder_var = tk.BooleanVar(value=True)
tk.Checkbutton(options_frame, text="Open folder after saving KML", variable=open_folder_var,
               font=("Segoe UI", 12), bg="#1e1e1e", fg="white", selectcolor="#34495e").pack(anchor="w")

# Place Types
place_frame = tk.LabelFrame(main_frame, text="Place Types", font=("Segoe UI", 12), bg="#1e1e1e", fg="white", padx=10, pady=5)
place_frame.pack(fill="x", pady=(0, 10))

place_types_checkbuttons = {
    "village": tk.BooleanVar(),
    "town": tk.BooleanVar(),
    "city": tk.BooleanVar(),
    "hamlet": tk.BooleanVar(),
    "locality": tk.BooleanVar(),
    "farm": tk.BooleanVar(),
    "isolated_dwelling": tk.BooleanVar()
}

# Create 2 rows of checkboxes
place_row1 = tk.Frame(place_frame, bg="#1e1e1e")
place_row1.pack(fill="x")
place_row2 = tk.Frame(place_frame, bg="#1e1e1e")
place_row2.pack(fill="x")

i = 0
for pt in place_types_checkbuttons:
    parent = place_row1 if i < 4 else place_row2
    tk.Checkbutton(parent, text=pt.capitalize(), variable=place_types_checkbuttons[pt],
                   font=("Segoe UI", 12), bg="#1e1e1e", fg="white", selectcolor="#34495e").pack(side="left", padx=10, pady=5)
    i += 1

# Button Frame
button_frame = tk.Frame(main_frame, bg="#1e1e1e")
button_frame.pack(pady=15)

ttk.Button(button_frame, text="Fetch Data", 
           command=lambda: threading.Thread(target=fetch_data_thread, daemon=True).start()).pack(side="left", padx=10)

ttk.Button(button_frame, text="Select Output Dir", 
           command=select_output_dir).pack(side="left", padx=10)

# Create a larger status display
status_frame = tk.Frame(main_frame, bg="#2a2a2a", padx=2, pady=2)
status_frame.pack(fill="x", pady=(10, 0))

status_label = tk.Label(status_frame, text="Ready to search", font=("Segoe UI", 12), bg="#1e1e1e", fg="white", padx=5, pady=5)
status_label.pack(fill="x")

# Footer with creator credits
tk.Label(root, text="Made by BennoGHG", font=("Segoe UI", 10), bg="#1e1e1e", fg="white").pack(side="bottom", pady=5)

# Try to load icons if available, don't crash if not found
try:
    root.iconbitmap(resource_path("icon.ico"))
except:
    pass

try:
    icon = tk.PhotoImage(file=resource_path("icon.png"))
    root.iconphoto(False, icon)
except:
    pass

# Default output directory
kml_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kml_output")
os.makedirs(kml_dir, exist_ok=True)

root.mainloop()
