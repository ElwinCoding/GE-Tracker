import requests

url = "https://prices.runescape.wiki/api/v1/osrs/mapping"

headers = {
    "User-Agent": "ID to item - @Roflnator#3778"
}

response = requests.get(url, headers=headers)
response = response.json()
# class to store the dictionaries
class database:
    def __init__(self):
        self.ItemID = {}
        for item in response:
            self.ItemID[str(item["id"])] = [item["name"], item.get("limit", 1)]

    def print_database(self):
        print(self.ItemID)

    def idLookup(self, id, index=None):
        if index == None:
            return self.ItemID[id]
        else:
            return self.ItemID[id][index]

guh = database()
# guh.print_database()
#print((guh.idLookup("27202")))