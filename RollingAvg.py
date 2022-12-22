import sys
import threading
import time
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from APIResources import APIResources

def main():
    headers = {
        "User-Agent": "dump watcher - @Roflnator#3778"
    }

    api = APIResources(headers=headers)
    samples = []
    while True:
        reply = api.getLatest()
        samples.append(reply)
        if len(samples) < 10:
            pass
        elif len(samples) == 61:
            samples.pop()
        processing_thread = threading.Thread(target=process, args=samples)
        processing_thread.start()
        time.sleep(60)
        processing_thread.join()


def process(samples):
    for sample in samples:
        pass




























if __name__ == "__main__":
    main()