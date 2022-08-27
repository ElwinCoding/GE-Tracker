import sys
import threading
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Package.APIResources import APIResources
import ItemID


def main():
    headers = {
        "User-Agent": "dump watcher - @Roflnator#3778"
    }

    api = APIResources(headers=headers)
    sample = []
    while True:
        reply = api.getLatest()
        sample.append(reply)
        if len(sample) < 10:
            print("guh")














if __name__ == "__main__":
    main()