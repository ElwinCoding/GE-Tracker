import requests
import logging
import argparse
from tabulate import tabulate
from item_def import *


class ParsedArguments:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-roi', action="store", help='Check for item ROI when flipping.')
        parser.add_argument(
            '-roi_sort',
            action="store",
            help='Sort ROI table by item, roi or volume. Type \'item\', \'roi\' or \'vol\' after the flag.'
        )
        parser.add_argument(
            '-roi_descending',
            action="store_true",
            help='Sort ROI in descending order.'
        )

        args = parser.parse_args()

        self.roi_flag = float(args.roi)
        self.roi_sort = args.roi_sort
        self.roi_descending = args.roi_descending


def main():
    arguments = ParsedArguments()

    headers = {
        'User-Agent': 'test_app',
        'From': 'christesar@yahoo.ca'
    }

    base_url = 'https://prices.runescape.wiki/api/v1/osrs'
    id_map = IDToItem()

    if arguments.roi_flag:
        reply = requests.get(base_url+"/5m", headers=headers)
        reply_json = reply.json()
        roi_table = []
        roi_headers = ["Item ID", "ROI %", "Avg. Volume"]

        for item_id in reply_json['data']:
            if int(item_id) < 27226:
                high_price = reply_json['data'][f'{item_id}']['avgHighPrice']
                low_price = reply_json['data'][f'{item_id}']['avgLowPrice']
                high_vol = reply_json['data'][f'{item_id}']['highPriceVolume']
                low_vol = reply_json['data'][f'{item_id}']['lowPriceVolume']
                avg_vol = (high_vol+low_vol)/2

                if high_price and low_price:
                    roi = ((high_price - low_price) / low_price) * 100
                    if roi > arguments.roi_flag:  # The ROI is larger than the threshold ROI
                        roi_table.append([
                            id_map.dict[f"{item_id}"],
                            f"{round(roi, 2)}%",
                            avg_vol
                        ])
        if arguments.roi_sort:
            roi_table = sort(roi_table, arguments.roi_sort, arguments.roi_descending)
        print(tabulate(roi_table, roi_headers, tablefmt="github"))
    # if arguments.dump_detect:


def sort(table, key, descending):
    if key == "item":
        return sorted(table, key=lambda x: x[0], reverse=descending)
    elif key == "roi":
        return sorted(table, key=lambda x: x[1], reverse=descending)
    elif key == "vol":
        return sorted(table, key=lambda x: x[2], reverse=descending)


if "__main__" == __name__:
    main()
