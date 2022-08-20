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
            self.ItemID[item["id"]] = [item["name"]]

    def print_database(self):
        print(self.ItemID)

    def IDLookup(self, ID):
        return self.ItemID[ID]

