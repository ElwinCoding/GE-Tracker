import requests

class APIResources:
    def __init__(self, headers):
        self.base_url = 'https://prices.runescape.wiki/api/v1/osrs'
        self.headers = headers

    def get5mUrl(self):
        return self.base_url + "/5m"

    def get1hUrl(self):
        return self.base_url + "/1h"

    def getTimeSeriesUrl(self):
        return self.base_url + "/timeseries"

    def getMappingUrl(self):
        return self.base_url + "/mapping"

    def getLatestUrl(self):
        return self.base_url + "mapping"

    def get5m(self, timestamp):
        return requests.get(self.get5mUrl(), headers=self.headers, params=timestamp)

    def get1h(self, timestamp: str = None):
        payload = {"timestamp": timestamp}
        return requests.get(self.get1hUrl(), headers=self.headers, params=payload)

    def getTimeSeries(self, item_id: str = None, timestep: str = None):
        payload = {"id": item_id, "timestep": timestep}
        return requests.get(self.getTimeSeriesUrl(), headers=self.headers, params=payload)

    def getLatest(self, item_id: str = None):
        payload = {"id": item_id}
        return requests.get(self.getLatestUrl(), headers=self.headers, params=payload)

    def getMapping(self):
        return requests.get(self.getLatestUrl(), headers=self.headers)


