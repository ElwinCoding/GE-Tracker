import collections

from APIResources import APIResources
from collections import deque

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}


class ItemQueues(dict):
    """
    class to store collection of queues for item prices
    """
    def __init__(self):
        super().__init__()
        self._initializeQueues()
        self.updateQueues()

    def _initializeQueues(self):
        """
        only creates queues for items with data from past 24h
        """
        api = APIResources(headers=headers)
        response = api.get24h()
        for item in response["data"]:
            high_price = response["data"][item]["avgHighPrice"]
            low_price = response["data"][item]["avgLowPrice"]
            if high_price is None or low_price is None:
                continue
            else:
                self[item] = {"highPrices": collections.deque([high_price], maxlen=10),
                              "lowPrices": collections.deque([low_price], maxlen=10),
                              "highRolling": 0,
                              "lowRolling": 0}

    def updateQueues(self):
        """
        updates queues in self
        """
        api = APIResources(headers=headers)
        response = api.getLatest()
        for item in self:
            high = response["data"][item]["high"]
            low = response["data"][item]["high"]
            self[item]["highPrices"].append(high)
            self[item]["lowPrices"].append(low)

    def getRolling(self):
        raise NotImplemented


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
