import time
import requests
import pandas as pd

data = pd.read_table("White.txt", header=None, names=["bulk"])

RGX_PATTERN = r"^(\d+) (.+?) \(([\w\d]+)\) (\d+[a-z]*) ?([A-Z])?$"

data[["Count", "Card_Name", "Set_Code", "Collector_nr", "Foil"]] = data[
    "bulk"
].str.extract(RGX_PATTERN)

json_responses = []

def get_magic_card(set_code, collector_number):
    # base_url = "https://api.scryfall.com/cards/named"
    # params = {"fuzzy": card_name}

    base_url = f"https://api.scryfall.com/cards/{set_code.lower()}/{collector_number}"
    response = requests.get(base_url, timeout=5)

    print(response.url)

    if response.status_code == 200:
        json_responses.append(response.json())
        print(f"Card added: {response.json()['name']}")
    else:
        print(f"Error: {response.status_code}")

for index, row in data.iterrows():
    get_magic_card(row['Set_Code'],row['Collector_nr'])
    time.sleep(1)

combined_data = pd.concat(
    [pd.json_normalize(response) for response in json_responses], ignore_index=True
)
combined_data.to_csv('card_info.csv')
print(combined_data.head(10))
