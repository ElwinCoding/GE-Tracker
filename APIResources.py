import requests
import time


class APIResourcesConstants:
    BASE_URL = 'https://prices.runescape.wiki/api/v1/osrs'
    FIVE_MINUTES = "/5m"
    TEN_MINUTES = "/10m"
    ONE_HOUR = "/1h"
    TWENTY_FOUR_HOURS = "/24h"
    TIME_SERIES = "/timeseries"
    MAPPING = "/mapping"
    LATEST = "/latest"


class APIResources:
    def __init__(self, headers):
        self.base_url = APIResourcesConstants.BASE_URL
        self.headers = headers

    def get5mUrl(self):
        return f"{self.base_url}{APIResourcesConstants.FIVE_MINUTES}"

    def get10mUrl(self):
        return f"{self.base_url}{APIResourcesConstants.TEN_MINUTES}"

    def get1hUrl(self):
        return f"{self.base_url}{APIResourcesConstants.ONE_HOUR}"

    def get24hUrl(self):
        return f"{self.base_url}{APIResourcesConstants.TWENTY_FOUR_HOURS}"

    def getTimeSeriesUrl(self):
        return f"{self.base_url}{APIResourcesConstants.TIME_SERIES}"

    def getMappingUrl(self):
        return f"{self.base_url}{APIResourcesConstants.MAPPING}"

    def getLatestUrl(self):
        return f"{self.base_url}{APIResourcesConstants.LATEST}"

    def get5m(self, timestamp: str = None):
        payload = {"timestamp": timestamp}
        return requests.get(self.get5mUrl(), headers=self.headers, params=payload).json()

    def get10m(self, timestamp=None):
        payload = {"timestamp": timestamp}
        return requests.get(self.get10mUrl(), headers=self.headers, params=payload).json()

    def get1h(self, timestamp: str = None):
        payload = {"timestamp": timestamp}
        return requests.get(self.get1hUrl(), headers=self.headers, params=payload).json()

    def get24h(self, timestamp: str = None):
        payload = {"timestamp": timestamp}
        return requests.get(self.get1hUrl(), headers=self.headers, params=payload).json()

    def getTimeSeries(self, item_id: str = None, timestep: str = None):
        payload = {"id": item_id, "timestep": timestep}
        return requests.get(self.getTimeSeriesUrl(), headers=self.headers, params=payload).json()

    def getLatest(self, item_id: str = None):
        payload = {"id": item_id}
        return requests.get(self.getLatestUrl(), headers=self.headers, params=payload).json()

    def getMapping(self):
        return requests.get(self.getMappingUrl(), headers=self.headers).json()

    def getVolume(self):
        return requests.get("https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json", headers=self.headers).json()

    def get5mMultiple(self, counter):
        base = time.time()
        # most recent 5m may take time to compile, 10m delay will prevent empty data field
        base = int(base - (base % 300) - 600)
        files = []
        for i in range(counter):
            payload = {"timestamp": str(base)}
            response = requests.get(self.get5mUrl(), headers=self.headers, params=payload).json()
            files.append(response)
            base -= 300
        return files

    def get10mMultiple(self, counter):
        base = time.time()
        # most recent 10m may result in emtpy data field, 20m delay to ensure data
        base = int(base - (base % 600) - 1200)
        files = []
        for i in range(counter):
            payload = {"timestamp": str(base)}
            response = requests.get(self.get5mUrl(), headers=self.headers, params=payload).json()
            files.append(response)
            base -= 600
        return files

    def get1hMultiply(self, counter):
        base = time.time()
        # most recent 1h may result in empty data field, 2h delay to ensure data
        base = int(base - (base % 3600) - 7200)
        files = []
        for i in range(counter):
            payload = {"timestamp": str(base)}
            response = requests.get(self.get5mUrl(), headers=self.headers, params=payload).json()
            files.append(response)
            base -= 3600
        return files
