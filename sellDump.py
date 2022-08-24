import requests
import ItemID

url_latest = "https://prices.runescape.wiki/api/v1/osrs/latest"
url_1h = "https://prices.runescape.wiki/api/v1/osrs/1h"
url_m = "https://prices.runescape.wiki/api/v1/osrs/10m"
url_24h = "https://prices.runescape.wiki/api/v1/osrs/24h"

headers = {
    "User-Agent": "dump watcher - @Roflnator#3778"
}

response_latest = requests.get(url_latest, headers=headers)
response_latest = response_latest.json()

response_1h = requests.get(url_1h, headers=headers)
response_1h = response_1h.json()

response_m = requests.get(url_m, headers=headers)
response_m = response_m.json()

response_24h = requests.get(url_m, headers=headers)
response_24h = response_24h.json()

print(response_m)