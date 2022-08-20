import requests
import ItemID

url = "https://prices.runescape.wiki/api/v1/osrs/latest"

headers = {
    "User-Agent": "margin check - @Roflnator#3778"
}

response = requests.get(url, headers=headers)
response = response.json()

