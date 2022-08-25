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
crashes = []
name = ItemID.itemID()

for item in response_10m["data"]:
    high = response_latest["data"][item]["high"]
    low = response_latest["data"][item]["low"]

    # try:
    #     avg = response_10m["data"][item]["avgHighPrice"]
    # except KeyError:
    #     continue

    try:
        volume = response_24h["data"][item]["highPriceVolume"] + response_24h["data"][item]["lowPriceVolume"]
    except KeyError:
        continue

    avg_buy = response_10m["data"][item]["avgHighPrice"]
    avg_sell = response_10m["data"][item]["avgLowPrice"]

    if avg_buy != None and high < low:
        difference = int((avg_buy - high)/avg_buy * 100)
        margin = low - high
        potential = margin * name.idLookup(item, 1)
        if difference >= 10 and potential >= 100000 and volume > name.idLookup(item,1):
            dumps.append([difference, item, high, low, volume, potential, volume])

    elif avg_sell != None and high > low:
        difference = int((avg_sell - low)/avg_sell * 100)
        margin = high - low
        potential = margin * name.idLookup(item, 1)
        if difference >= 10 and potential >= 100000 and volume > name.idLookup(item,1):
            crashes.append([difference, item, high, low, volume, potential, volume])

dumps.sort(reverse= True)
crashes.sort(reverse= True)

if len(dumps) != 0:
    print(f"|{'':-^150}|")
    print(f"|{'Dumps':^150}|")
    print(f"|{'':-^150}|")
    print(f"|{'Item':^30}|{'Buy Price':^29}|{'Sell Price':^29}|{'24h Volume':^29}|{'Potential':^29}|")
    print(f"|{'':-^150}|")
    for item in dumps:
        print(f"|{name.idLookup(item[1],0):<30}|{item[2]:>29}|{item[3]:>29}|{item[4]:>29}|{item[5]:>29}|")
else:
    print("No dumps were detected")

if len(crashes) != 0:
    print(f"|{'':-^150}|")
    print(f"|{'Crashes':^150}|")
    print(f"|{'':-^150}|")
    print(f"|{'Item':^30}|{'Buy Price':^29}|{'Sell Price':^29}|{'24h Volume':^29}|{'Potential':^29}|")
    print(f"|{'':-^150}|")
    for item in crashes:
        print(f"|{name.idLookup(item[1],0):<30}|{item[2]:>29}|{item[3]:>29}|{item[4]:>29}|{item[5]:>29}|")
    print(f"|{'':-^150}|")
else:
    print("No crashes were detected")
# now = time.time()
# print(now / 300)
