import json

from app.services.metrics.save_in_click import save_in_click


def check_tpm_metrics():
    # Open the JSON file
    file_path = '../../../tmp.json'
    with open(file_path, 'r') as f:
        # Load the JSON data as an array of objects
        data = json.load(f)

    # Loop through the array of objects and print them to the console
    for obj in data:
        try:
            save_in_click(obj)
        except Exception as e:
            print(e)

    # Remove the first object from the array

    # Write the updated array back to the file
    with open(file_path, 'w') as f:
        json.dump([], f)
