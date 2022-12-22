from APIResources import APIResources

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}


class ItemIDConstants:
    ITEM_NAME = 0
    ITEM_LIMIT = 1


class ItemID:
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
            self.item_ids[str(item["id"])] = [item["name"], item.get("limit", 1)]

    def printItemIDsMapping(self):
        print(self.item_ids)

    def idLookup(self, id, index=None):
        if index is None:
            return self.item_ids[id]
        else:
            return self.item_ids[id][index]

    def getName(self, id: str) -> str:
        return self.item_ids[id][ItemIDConstants.ITEM_NAME]

    def getLimit(self, id: str) -> int:
        return self.item_ids[id][ItemIDConstants.ITEM_LIMIT]
