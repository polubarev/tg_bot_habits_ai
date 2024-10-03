import os
import json
import pandas as pd

# Directory containing the JSON files
json_folder = 'extracted_habits'

# List to store data
data = []

# Read all JSON files from the directory with proper encoding
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as f:
            json_data = json.load(f)

            # Flatten the JSON structure
            for date_key, entry in json_data.items():
                flattened_entry = {'datetime': date_key}  # Add the date_key as 'datetime' field
                flattened_entry.update(entry.get('habits', {}))  # Add all 'habits' fields
                flattened_entry['diary'] = entry.get('diary', '')  # Add 'diary' field

                data.append(flattened_entry)

# Convert list of JSON objects to DataFrame
df = pd.json_normalize(data)
print(df)
df.to_csv('database.csv', index=False,)