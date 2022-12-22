from APIResources import APIResources

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}


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
            name=None
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


class ItemMap:
    """
    Class to store the mappings between item ID and item name.
    """
    def __init__(self):
        self.item_ids = {}
        self._initializeItemIDs()

    def _initializeItemIDs(self):
        api = APIResources(headers=headers)
        response = api.getMapping()
        for item in response:
            self.item_ids[str(item["id"])] = ItemInfo.fromDict(item)
            print(self.item_ids[str(item["id"])].__dict__)

    def printItemIDsMapping(self):
        print(self.item_ids)

    def idLookup(self, id: str) -> ItemInfo:
        return self.item_ids[id]

