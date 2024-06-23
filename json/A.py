import json

def extract_showValue(data, indent=0):
    if isinstance(data, dict):
        if 'showValue' in data:
            print(' ' * indent + data['showValue'])
        if 'toolTreeNodeVOList' in data:
            for item in data['toolTreeNodeVOList']:
                extract_showValue(item, indent + 2)
    elif isinstance(data, list):
        for item in data:
            extract_showValue(item, indent)

try:
    with open('1.json', 'r') as f:
        print("Reading JSON data...")
        data = json.load(f)
        print("JSON data read successfully.")
except Exception as e:
    print("Failed to read JSON data: " + str(e))
else:
    print("Extracting showValue...")
    extract_showValue(data)
    print("Extraction complete.")