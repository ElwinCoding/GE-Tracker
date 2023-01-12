from APIResources import APIResources
from ItemID import ItemMap
import tabulate

headers = {
    "User-Agent": "dump watcher - @Roflnator#3778"
}

api = APIResources(headers=headers)

response_latest = api.getLatest()

response_1h = api.get1h()

response_10m = api.get10m()

response_24h = api.get24h()

volume = api.getVolume()

dumps = []
crashes = []
item_map = ItemMap()


def volume_check(volume, margin, item):
    if margin >= 200000:
        return True
    elif margin <= 200000 and volume > item_map[item].limit:
        return True
    else:
        return False


for item in response_10m["data"]:
    high = response_latest["data"][item]["high"]
    low = response_latest["data"][item]["low"]

    item_volume = volume[item].get("volume")

    avg_buy = response_10m["data"][item]["avgHighPrice"]
    avg_sell = response_10m["data"][item]["avgLowPrice"]

    if avg_buy is not None and high < low:
        difference = int((avg_buy - high)/avg_buy * 100)
        margin = low - high
        potential = margin * item_map[item].limit
        if difference >= 5 and potential >= 500000 and volume_check(item_volume, margin, item):
            dumps.append([item_map[item].name, high, low, item_volume, item_map[item].limit, potential])

    elif avg_sell is not None and high > low:
        difference = int((avg_sell - low)/avg_sell * 100)
        margin = high - low
        potential = margin * item_map[item].limit
        if difference >= 5 and potential >= 500000 and volume_check(item_volume, margin, item):
            crashes.append([item_map[item].name, high, low, item_volume, item_map[item].limit, potential])

dumps.sort(key=lambda x: x[-1], reverse=True)
crashes.sort(key=lambda x: x[-1], reverse=True)

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
