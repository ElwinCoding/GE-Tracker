import sys
import threading
import time
from os import path
import ItemID
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from APIResources import APIResources

collection = ItemID.ItemCollection()
queue = ItemID.ItemQueues(collection)
queue.dump_checker()