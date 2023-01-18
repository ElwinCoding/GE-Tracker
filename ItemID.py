import numpy as np
import time
from APIResources import APIResources
from collections import deque

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}


class ItemCollection(dict):
    """
    class to store info and pricing of an item
    """
    def __init__(self):
        super().__init__()
        self._initializeDatabase()
        self.updateVolume()
        self.updatePrices()

    def _initializeDatabase(self):
        """
        compares Item IDs between mapping and latest to create entries
        """
        api = APIResources(headers=headers)
        mapping = api.getMapping()
        response = api.getLatest()["data"]
        for item in mapping:
            if response.get(str(item["id"])) is None:
                continue
            else:
                self[str(item["id"])] = Item(ItemInfo.fromDict(item), ItemPricing())

    def updateVolume(self):
        api = APIResources(headers=headers)
        response = api.getVolume()
        # remove Jagex and Bot timestamp keys
        response.popitem()
        response.popitem()
        for item in self:
            self[item].item_pricing.volume = response[item].get("volume", None)

    def updatePrices(self):
        api = APIResources(headers=headers)
        response = api.getLatest()["data"]
        for item in self:
            self[item].item_pricing.high = response[item]["high"]
            self[item].item_pricing.low = response[item]["low"]


class Item:
    def __init__(self, item_info=None, item_pricing=None):
        self.item_info = item_info
        self.item_pricing = item_pricing


class ItemPricing:
    def __init__(self):
        self.volume = None
        self.high = None
        self.low = None

    def printPricing(self):
        print("High:", self.high, "| Low:", self.low, "| Volume:", self.volume)


class ItemInfo:
    def __init__(
            self,
            examine=None,
            id=None,
            members=None,
            lowalch=None,
            limit=None,
            value=None,
            highalch=None,
            icon=None,
            name=None,
    ):
        self.examine = examine
        self.id = id
        self.members = members
        self.lowalch = lowalch
        self.limit = limit
        self.value = value
        self.highalch = highalch
        self.icon = icon
        self.name = name

    @classmethod
    def fromDict(cls, dict):
        return ItemInfo(
            examine=dict.get('examine', None),
            id=dict.get('id', None),
            members=dict.get('members', None),
            lowalch=dict.get('lowalch', None),
            limit=dict.get('limit', 0),
            value=dict.get('value', None),
            highalch=dict.get('highalch', None),
            icon=dict.get('icon', None),
            name=dict.get('name', None)
        )


class ItemMap(dict):
    """
    Class to store the mappings between item ID and item name.
    """
    def __init__(self):
        super().__init__()
        self._initializeItemIDs()

    def _initializeItemIDs(self):
        api = APIResources(headers=headers)
        response = api.getMapping()
        for item in response:
            self[str(item["id"])] = ItemInfo.fromDict(item)

    def printItemIDsMapping(self):
        print(self)

    def idLookup(self, id: str) -> ItemInfo:
        return self[id]


class ItemQueues(dict):
    """
    class to store collection of queues for item prices
    """
    MAX_LEN_STORED = 20
    DATA = "data"
    AVG_HIGH_PRICE = "avgHighPrice"
    AVG_LOW_PRICE = "avgLowPrice"
    HIGH_VOLUME = 100000
    POTENTIAL = 500000

    def __init__(self, item_collection: ItemCollection):
        super().__init__()
        self.item_collection = item_collection
        self.api = APIResources(headers=headers)
        self._initializeQueues()
        self.updateQueues()
        self.updateRolling()

    def _initializeQueues(self):
        """
        only creates queues for items with data from past 24h
        """
        response = self.api.get24h()
        for item in response[self.DATA]:
            high_price = response[self.DATA][item][self.AVG_HIGH_PRICE]
            low_price = response[self.DATA][item][self.AVG_LOW_PRICE]
            if high_price is None or low_price is None:
                continue
            else:
                self[item] = {"highPrices": deque([high_price], maxlen=self.MAX_LEN_STORED),
                              "lowPrices": deque([low_price], maxlen=self.MAX_LEN_STORED),
                              "highRolling": 0,
                              "lowRolling": 0,
                              "highTime": 0,
                              "lowTime": 0}

        data_points = self.api.get5mMultiple(self.MAX_LEN_STORED - 2)
        for id, prices in self.items():
            for i in range(self.MAX_LEN_STORED - 2):
                item = data_points[i]["data"].get(id)
                if item is None:
                    continue
                high, low = item["avgHighPrice"], item["avgLowPrice"]
                # if either is None, set to most recent price point
                if high is None:
                    high = prices["highPrices"][-1]
                if low is None:
                    low = prices["lowPrices"][-1]
                prices["highPrices"].append(high)
                prices["lowPrices"].append(low)

    def updateQueues(self):
        """
        updates queues in self
        """
        response = self.api.getLatest()
        for id, prices in self.items():
            high = response[self.DATA][id]["high"]
            low = response[self.DATA][id]["low"]
            high_time = response[self.DATA][id]["highTime"]
            low_time = response[self.DATA][id]["lowTime"]
            prices["highPrices"].append(high)
            prices["lowPrices"].append(low)
            prices["highTime"] = high_time
            prices["lowTime"] = low_time

    def updateRolling(self):
        def f(idx, price, denominator): return price * (idx / denominator)
        for id, queue in self.items():
            # highPrices and lowPrices should always be the same length
            denominator = sum(range(1, len(queue["highPrices"]) + 1))
            high_prices_weighted = [f(i, high_price, denominator) for i, high_price in enumerate(queue['highPrices'], start=1)]
            low_prices_weighted = [f(i, low_price, denominator) for i, low_price in enumerate(queue['lowPrices'], start=1)]
            high_rolling_average = round(sum(high_prices_weighted))
            low_rolling_average = round(sum(low_prices_weighted))
            self[id]["highRolling"] = high_rolling_average
            self[id]["lowRolling"] = low_rolling_average

    def _filter(self, volume, limit, margin, high_time, low_time):
        # if no volume in past 24h
        if volume is None:
            return 0
        # if latest buy and sell transaction occurred over 5m ago
        current = time.time()
        if current - high_time > 300 and current - low_time > 300:
            return 0
        # if buy limit is unknown
        elif limit is None:
            potential = volume * 0.05 * margin
        # if item is high volume
        elif volume >= self.HIGH_VOLUME:
            potential = limit * margin
        # if item is low volume
        else:
            potential = min(volume * 0.03, limit) * margin

        return round(potential) if potential >= self.POTENTIAL else 0

    def dumpChecker(self):
        """
        compare rolling and latest to find large differences
        """
        buy_dumps = []
        sell_dumps = []
        for id, prices in self.items():
            volume, limit, name = (
                self.item_collection[id].item_pricing.volume,
                self.item_collection[id].item_info.limit,
                self.item_collection[id].item_info.name,
            )
            high_latest, high_previous = prices["highPrices"][-1], prices["highPrices"][-2]
            low_latest = prices["lowPrices"][-1]
            high_time, low_time = prices["highTime"], prices["lowTime"]

            # Compares most recent buy price to rolling buy price and finds percent difference
            if round((prices["highRolling"] - high_latest) / prices["highRolling"] * 100) >= 5:
                margin = high_previous - high_latest
                potential = self._filter(volume, limit, margin, high_time, low_time)
                if potential:
                    buy_dumps.append([name, high_previous, high_latest, volume, limit, potential])
            # Compares most recent sell price to rolling buy price and finds percentage difference
            elif round((prices["lowRolling"] - low_latest) / prices["lowRolling"] * 100) >= 5:
                margin = high_latest - low_latest
                potential = self._filter(volume, limit, margin, high_time, low_time)
                if potential:
                    sell_dumps.append([name, high_latest, low_latest, volume, limit, potential])
            else:
                continue
        buy_dumps.sort(key=lambda x: x[-1], reverse=True)
        sell_dumps.sort(key=lambda x: x[-1], reverse=True)

        return buy_dumps[:7], sell_dumps[:7]
