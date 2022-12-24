from APIResources import APIResources

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}


class PriceDatabase(dict):
    def __init__(self):
        super().__init__()


class ItemDatabase(dict):
    """
    class to store info and pricing of an item
    """
    def __init__(self):
        super().__init__()
        self._initializeDatabase()
        self.updateVolume()

    def _initializeDatabase(self):
        api = APIResources(headers=headers)
        response = api.getMapping()
        for item in response:
            self[str(item["id"])] = Item(ItemInfo.fromDict(item), ItemPricing())

    def updateVolume(self):
        api = APIResources(headers=headers)
        response = api.getVolume()
        # remove Jagex and Bot timestamp keys
        response.popitem()
        response.popitem()
        for item in response:
            self[item].item_pricing.volume = response[item].get("volume", None)


class Item:
    def __init__(self, item_info=None, item_pricing=None):
        self.item_info = item_info
        self.item_pricing = item_pricing


class ItemPricing:
    def __init__(self):
        self.volume = None
        self.rolling_high = None
        self.rolling_low = None
        self.high = None
        self.low = None


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
