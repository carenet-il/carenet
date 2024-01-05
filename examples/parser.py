import json

# Replace 'your_file.json' with the path to your JSON file
file_path = './n12_feed.json'

# Reading data from the file
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Filtering records with 'medical' or 'sport' in subcats
filtered_records = []
for record in json_data:
    if record.get("event_type", None) == "offer_help":
        for subcat in record.get("subcats", []):
            if subcat["name"] in ["רפואה משלימה", "בריאות הנפש", "יוגה ומיינדפולנס", "רפואה", "טיפולים הוליסטיים",
                                  "סיוע כללי"]:
                filtered_records.append(record)

            # if subcat["name"] in ["רפואה משלימה", "בריאות הנפש", "טיפולים הוליסטיים"]:
            #     filtered_records.append(record)
            #     break  # Break the inner loop if a matching subcat is found

print("found results", str(len(filtered_records)))

import requests


def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()
    return data.get("display_name")


for r in filtered_records:
    print("******")
    print(r["content"])
    location = reverse_geocode(r["location"]["lat"], r["location"]["lon"])
    print("Location:", location)
    print("******")

# Now filtered_records contains all the records with 'medical' or 'sport' subcategories
# Define the path for the new JSON file
output_file_path = './filtered_records.json'

# Writing the filtered records to a new JSON file
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(filtered_records, file, ensure_ascii=False, indent=4)
