import json

def process_entry(entry):
    # Check if 'LEFT' or 'RIGHT' is missing
    if 'LEFT' not in entry:
        entry['LEFT'] = 'L' + entry['RIGHT'][1:]
    elif 'RIGHT' not in entry:
        entry['RIGHT'] = 'R' + entry['LEFT'][1:]

# Load JSON file
input_file_path = 'modified.json'  #input
output_file_path = 'data.json'  #output

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Process each entry in the JSON data
for entry_key, entry_value in data.items():
    process_entry(entry_value)

# Save the modified data to a new JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=2)

print(f'Processed data saved to {output_file_path}')
