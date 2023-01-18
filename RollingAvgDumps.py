import time
import ItemID
import tabulate
import os

headers = {
    "User-Agent": "dump watcher - @Roflnator#3778"
}


collection = ItemID.ItemCollection()
queues = ItemID.ItemQueues(collection)
columns = ["Item", "Buy Price", "Sell Price", "24h Volume", "Limit", "Potential"]

while True:
    lists = queues.dumpChecker()
    # print
    print(time.asctime(time.localtime(time.time())))
    print(f"{'':->5}")
    print("Dumps")
    print(f"{'':->5}")
    print(tabulate.tabulate(lists[0], headers=columns, tablefmt="github"))
    print(f"{'':->7}")
    print("Crashes")
    print(f"{'':->7}")
    print(tabulate.tabulate(lists[1], headers=columns, tablefmt="github"))
    print("\n")
    # sleep until latest updates (1 minute)
    countdown = 60 - (time.time() % 60)
    # extra time to allow api to update
    time.sleep(countdown)
    # update prices
    queues.updateQueues()
    queues.updateRolling()



