import json

def createJsonFile(json_data):
    try:
        # Save the json data in a file
        json_file = "processing_stats.json"
        with open(f"output/{json_file}", "w", encoding="utf-8") as file:
           json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"The json file '{json_file}' has been created")
    except (ValueError, TypeError):
        return False