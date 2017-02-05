import json

FILENAME = "settings.json"


def get_all():
    with open(FILENAME) as file:
        data = json.load(file)
        return data


def get_key():
    with open(FILENAME) as file:
        data = json.load(file)
        if len(data["api_key"]) == 0:
            raise ValueError("No key found.")

        return data["api_key"]


def update_date(old_data, date):
    old_data["last_date"] = str(date)
    with open(FILENAME, "w") as file:
        json.dump(old_data, file, indent=4)
