import requests
from ItemID import ItemMap
import time
import tabulate

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
crashes = []
item_map = ItemMap()

def volume_check(volume, margin, item):
    if margin >= 200000:
        return True
    elif margin <= 200000 and volume > item_map.idLookup(item).limit:
        return True
    else:
        return False

for item in response_10m["data"]:
    high = response_latest["data"][item]["high"]
    low = response_latest["data"][item]["low"]

    try:
        volume = response_24h["data"][item]["highPriceVolume"] + response_24h["data"][item]["lowPriceVolume"]
    except KeyError:
        continue

    avg_buy = response_10m["data"][item]["avgHighPrice"]
    avg_sell = response_10m["data"][item]["avgLowPrice"]

    if avg_buy != None and high < low:
        difference = int((avg_buy - high)/avg_buy * 100)
        margin = low - high
        potential = margin * item_map.idLookup(item).limit
        if difference >= 10 and potential >= 100000 and volume_check(volume, margin, item):
            dumps.append([item_map.idLookup(item).name, high, low, volume, item_map.idLookup(item).limit, potential])

    elif avg_sell != None and high > low:
        difference = int((avg_sell - low)/avg_sell * 100)
        margin = high - low
        potential = margin * item_map.idLookup(item).limit
        if difference >= 10 and potential >= 100000 and volume_check(volume, margin, item):
            crashes.append([item_map.idLookup(item).name, high, low, volume, item_map.idLookup(item).limit, potential])

dumps.sort(reverse= True)
crashes.sort(reverse= True)

columns = ["Item", "Buy Price", "Sell Price", "24h Volume", "Limit", "Potential"]

if len(dumps) != 0:
    print(f"{'':->5}")
    print("Dumps")
    print(f"{'':->5}")
    print(tabulate.tabulate(dumps, headers=columns, tablefmt="github"))
else:
    print("No dumps were detected")

if len(crashes) != 0:
    print(f"{'':->7}")
    print("Crashes")
    print(f"{'':->7}")
    print(tabulate.tabulate(crashes, headers=columns, tablefmt="github"))

else:
    print("No crashes were detected")
# now = time.time()
# print(now / 300)
