import subprocess
import sys
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import os
import threading

# Auto-install missing dependencies
def install_requirements():
    packages = ["requests"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_requirements()

# Country to Wikidata QID mapping
country_qids = {
    "Germany": "Q183",
    "France": "Q142",
    "United States": "Q30",
    "Italy": "Q38",
    "Spain": "Q29",
    "Canada": "Q16",
    "Australia": "Q408",
    "United Kingdom": "Q145",
    "Japan": "Q17",
    "Russia": "Q159",
    "Brazil": "Q155",
    "India": "Q668",
    "Mexico": "Q96",
    "South Africa": "Q258",
    "Argentina": "Q414",
    "Sweden": "Q34",
    "Norway": "Q20",
    "Finland": "Q33",
    "Netherlands": "Q55",
    "Belgium": "Q31",
    "Poland": "Q36",
    "Switzerland": "Q39",
    "Austria": "Q40",
    "Denmark": "Q35",
    "South Korea": "Q884",
    "Turkey": "Q43",
    "New Zealand": "Q664",
    "Chile": "Q298",
    "Israel": "Q801",
    "Portugal": "Q45",
    "Czech Republic": "Q213",
    "Greece": "Q41",
    "Egypt": "Q79",
    "Singapore": "Q334",
    "Malaysia": "Q833",
    "Thailand": "Q869",
    "Philippines": "Q928",
    "Indonesia": "Q252",
    "Vietnam": "Q881",
    "Ukraine": "Q212",
    "Hungary": "Q28",
    "Romania": "Q218",
    "Belarus": "Q184",
    "Ireland": "Q27"
}

def generate_query(country, suffix, place_types):
    qid = country_qids.get(country)
    if not qid:
        return None

    place_filter = "|".join(place_types)
    query = f"""
    [out:json][timeout:1000];
    area["wikidata"="{qid}"]->.searchArea;
    (
      node["place"~"^{place_filter}$"]["name"~"{suffix}$"](area.searchArea);
    );
    out;
    """
    return query

def fetch_data_thread():
    country = country_combobox.get()
    suffix = suffix_entry.get().lstrip('-')  # Remove leading hyphen
    place_types = [pt for pt in place_types_checkbuttons if place_types_checkbuttons[pt].get()]
    if not country or not suffix or not place_types:
        messagebox.showerror("Error", "Please fill out all fields.")
        return

    query = generate_query(country, suffix, place_types)
    if not query:
        messagebox.showerror("Error", "Invalid country.")
        return

    overpass_url = "https://overpass-api.de/api/interpreter"
    status_label.config(text="The script is working... Please wait.")

    try:
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()

        if len(data["elements"]) > 0:
            save_to_kml(data, country, suffix)
        else:
            messagebox.showinfo("No Data", "No matching data found.")
    except Exception as e:
        messagebox.showerror("Error", f"API error: {e}")

    status_label.config(text="")

def save_to_kml(data, country, suffix):
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")

    try:
        for element in data.get("elements", []):
            if element["type"] == "node":
                name = element["tags"].get("name", "Unknown")
                lat = element["lat"]
                lon = element["lon"]

                placemark = ET.SubElement(document, "Placemark")
                ET.SubElement(placemark, "name").text = name
                point = ET.SubElement(placemark, "Point")
                ET.SubElement(point, "coordinates").text = f"{lon},{lat}"

        kml_str = ET.tostring(kml, encoding="utf-8").decode()
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, f"{country.lower()}--{suffix}.kml")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(kml_str)

        messagebox.showinfo("Saved", f"File saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

# UI Setup
root = tk.Tk()
root.title("Overpass Query Tool")
root.geometry("800x600")
root.configure(bg="#1e1e1e")
root.eval('tk::PlaceWindow . center')
root.resizable(True, True)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=8,
                background="#2a2a2a", foreground="white", borderwidth=0, relief="flat")
style.map("TButton", background=[("active", "#3498db")], foreground=[("active", "#ffffff")])

tk.Label(root, text="Select Country:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(pady=10)
country_combobox = ttk.Combobox(root, values=sorted(country_qids.keys()), font=("Segoe UI", 12))
country_combobox.pack(pady=10, padx=20, fill="x")

tk.Label(root, text="Suffix (e.g., 'ach'):", font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(pady=10)
suffix_entry = tk.Entry(root, font=("Segoe UI", 12))
suffix_entry.pack(pady=10, padx=20, fill="x")

tk.Label(root, text="Select Place Types:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(pady=10)
place_types_checkbuttons = {
    "village": tk.BooleanVar(),
    "town": tk.BooleanVar(),
    "city": tk.BooleanVar(),
    "road": tk.BooleanVar()
}
for pt in place_types_checkbuttons:
    tk.Checkbutton(root, text=pt.capitalize(), variable=place_types_checkbuttons[pt],
                   font=("Segoe UI", 12), bg="#1e1e1e", fg="white", selectcolor="#34495e").pack(pady=5)

status_label = tk.Label(root, text="", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
status_label.pack(pady=10)

ttk.Button(root, text="Fetch Data", command=lambda: threading.Thread(target=fetch_data_thread, daemon=True).start()).pack(pady=20)

tk.Label(root, text="Made by BennoGHG", font=("Segoe UI", 10), bg="#1e1e1e", fg="white").pack(side="bottom", pady=10)

root.mainloop()

