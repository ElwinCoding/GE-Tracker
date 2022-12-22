import json

with open("mapping.json") as file:
    map = json.load(file)

# class to store the dictionaries
class ItemID:
    def __init__(self):
        self.ItemID = {}
        for item in map:
            self.ItemID[str(item["id"])] = [item["name"], item.get("limit", 1)]

    def print_database(self):
        print(self.ItemID)

    def idLookup(self, id, index=None):
        if index == None:
            return self.ItemID[id]
        else:
            return self.ItemID[id][index]
