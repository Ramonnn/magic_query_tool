import requests
import pandas as pd

data = pd.read_table("White.txt", header=None, names=["bulk"])

RGX_PATTERN = r"^(\d+) (.+?) \(([\w\d]+)\) (\d+p?\d*) ?([A-Z])?$"

data[["Count", "Card_Name", "Set_Code", "Collector_nr", "Foil"]] = data[
    "bulk"
].str.extract(RGX_PATTERN)


def get_magic_card(card_name):
    base_url = "https://api.scryfall.com/cards/named"
    params = {"fuzzy": card_name}

    response = requests.get(base_url, params=params, timeout=5)

    if response.status_code == 200:
        card_data = response.json()
        return card_data

    print(f"Error: {response.status_code}")
    return None


result = get_magic_card(data["Card_Name"][5])

if result:
    print(f"Name: {result['name']}")
    print(f"Type: {result['type_line']}")
    print(f"Mana Cost: {result['mana_cost']}")
else:
    print("Card not found or error in fetching data.")


print(data.head(10))
