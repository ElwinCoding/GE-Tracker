import requests
import ItemID
import time

url_latest = "https://prices.runescape.wiki/api/v1/osrs/latest"
url_1h = "https://prices.runescape.wiki/api/v1/osrs/1h"
url_10m = "https://prices.runescape.wiki/api/v1/osrs/10m"
url_24h = "https://prices.runescape.wiki/api/v1/osrs/24h"

headers = {
    "User-Agent": "dump watcher - @Roflnator#3778"
}

response_latest = requests.get(url_latest, headers=headers)
response_latest = response_latest.json()

response_1h = requests.get(url_1h, headers=headers)
response_1h = response_1h.json()

response_10m = requests.get(url_10m, headers=headers)
response_10m = response_10m.json()

response_24h = requests.get(url_24h, headers=headers)
response_24h = response_24h.json()

dumps = []
name = ItemID.itemID()

for item in response_10m["data"]:
    high = response_latest["data"][item]["high"]
    low = response_latest["data"][item]["low"]

    try:
        avg = response_10m["data"][item]["avgHighPrice"]
    except KeyError:
        continue

    try:
        volume = response_24h["data"][item]["highPriceVolume"] + response_24h["data"][item]["lowPriceVolume"]
    except KeyError:
        continue

    if avg != None and high < low:
        difference = int((avg - high)/avg * 100)
        margin = low - high
        potential = margin * name.idLookup(item, 1)
        if difference >= 10 and potential >= 100000 and volume > name.idLookup(item,1):
            dumps.append([difference, item, high, low, volume, potential])

dumps.sort(reverse= True)

for x in dumps:
    print(name.idLookup(x[1]), "buy price:", x[2], "| sell price:", x[3], "| 24h volume:", x[4], "| potential:", x[5])


# now = time.time()
# print(now / 300)
