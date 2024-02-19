from PIL import Image
import pytesseract
import re
import json

# Set path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Admin\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

def process_img(file_path):
    # Open the image and convert text to string using OCR
    input_string = pytesseract.image_to_string(Image.open(f'{file_path}'))

    # Process string to get rid of unneeded characters/fix common mistakes/excess whitespace/etc
    pattern = re.compile(r'\b(?:USO5|USOS5|USOS)-\d+\b')
    output_string = re.sub(pattern, '', input_string)
    output_string = output_string.replace('£','E')
    output_string = output_string.replace('O','0')
    output_string = output_string.replace('a','8')
    output_string = output_string.replace('s','5')
    #output_string = output_string.replace('I','1')
    output_string = ''.join(filter(lambda c: c.isalnum() or c.isspace(),output_string)) #remove any non alphanumeric or space characters

    #remove empty lines
    lines = [line for line in output_string.splitlines() if line.strip()]
    output_string = '\n'.join(lines)

    #remove excess spaces
    lines = [ ' '.join(line.split()) for line in output_string.splitlines()]
    output_string = '\n'.join(lines)

    return output_string

def update_data(input_string, data):
    # Regex pattern to extract code, side, and value
    pattern = re.compile(r'([A-Z]+\d+) (R\d|L\d)(\S*)')
    # Iterate over each line and extract information
    for line in input_string.splitlines():
        matches = pattern.findall(line)
        for match in matches:
            code, side, value = match
            if code not in data:
                data[code] = {}

            #determine if right or left for entry
            if side.startswith('R'):
                sidestr = 'RIGHT'
            else:
                sidestr = "LEFT"

            #add side to front of value (i.e: R2/R1/L2/L1)
            value = side + value
            #update data
            data[code][sidestr] = value

# Create a dictionary to store the data from each img
data = {}

# Process each image and store data
for i in range(1,10):
    file_path = f'img{i}.jpg'
    string = process_img(file_path)
    print(string)
    update_data(string, data)


# Convert the data dictionary to JSON format and save it
output_file_path = "output_data1.json"
json_output = json.dumps(data,indent = 2)
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=2)

# Print the JSON output
print(json_output)
print(data)

