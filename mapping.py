import requests
import json

url = "https://prices.runescape.wiki/api/v1/osrs/mapping"

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}

response = requests.get(url, headers=headers)
response = response.json()

with open("mapping.json", "w") as file:
    json.dump(response, file)