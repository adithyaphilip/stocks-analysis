from bs4 import BeautifulSoup
import pandas as pd

import subprocess
import pickle
import time
import threading
import sys
import multiprocessing.pool as mpool
import urllib.parse

FIRST_DATE_FMT = "01-01-%d"
LAST_DATE_FMT = "31-12-%d"

URL = "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=%s" \
      "&segmentLink=3&symbolCount=2&series=ALL&dateRange=+&fromDate=%s&toDate=%s&dataType=PRICEVOLUMEDELIVERABLE"


def convert_html_to_csv(html, symbol):
    soup = BeautifulSoup(html, "lxml")
    div = soup.find('div', {'id': 'csvContentDiv'})
    if div is None:
        return []
    div_csv = div.contents[0]
    csv_rows = []
    for line in div_csv.strip().split(":"):
        # we want the symbol name to be the latest symbol name
        csv_rows.append(",".join([symbol] + [field.strip()[1:-1].strip() for field in line.split(",")[1:]]))

    return csv_rows[:-1]


def get_html_response(symbol, start_date, end_date):
    while True:
        try:
            return subprocess.check_output("./curl.sh %s %s %s 2> /dev/null"
                                           % (urllib.parse.quote_plus(symbol), start_date, end_date),
                                           shell=True)
        except Exception as e:
            print(e)


def get_data_for_wrapper(args):
    return get_data_for(symbol=args[0], start_year=args[1], end_year=args[2])


def get_data_for(symbol: str, start_year: int, end_year: int):
    csv_rows = []
    # url_map = {URL % (symbol, FIRST_DATE_FMT % year, LAST_DATE_FMT % year): symbol
    #            for symbol in symbols for year in reversed(range(start_year, end_year + 1))}
    # pending_reqs = [grequests.get(url) for url in url_map.keys()]
    # while len(pending_reqs) != 0:
    #     failed = []
    #     for result in grequests.imap(requests=pending_reqs,
    #                                  size=300,
    #                                  exception_handler=lambda request, exception: failed.append(request)):
    #         if result is None:
    #             continue
    #         res_rows = convert_html_to_csv(html=result.content.decode("utf-8"), symbol=url_map[result.url])
    #         if len(csv_rows) != 0:
    #             # we already have the header
    #             res_rows = res_rows[1:]
    #         csv_rows.extend(res_rows)
    #     pending_reqs = failed
    for year in reversed(range(start_year, end_year + 1)):
        res_rows = convert_html_to_csv(html=get_html_response(symbol=symbol,
                                                              start_date=FIRST_DATE_FMT % year,
                                                              end_date=LAST_DATE_FMT % year),
                                       symbol=symbol)
        if len(res_rows) <= 1:
            break
        if len(csv_rows) != 0:
            # we already have the header
            res_rows = res_rows[1:]
        csv_rows.extend(res_rows)

    return csv_rows


def get_symbols_to_fetch():
    fname = "sec_bhavdata_full.csv"
    df = pd.read_csv(fname)
    return set(df[df[' SERIES'] == ' EQ']['SYMBOL'].unique())


def main():
    symbols = list(get_symbols_to_fetch())
    symbols.sort()
    for symbol in symbols:
        print(symbol)
    return
    num = 16
    ctr = 0
    csv_rows = []
    print(0.0, time.time())
    # return
    # threads = [threading.Thread(target=get_data_for,
    #                             kwargs={"symbol": symbol, "start_year": 2006, "end_year": 2016})
    #            for symbol in symbols[:10]]
    #
    # for thread in threads:
    #     thread.start()
    #
    # ctr = 0
    # for thread in threads:
    #     thread.join()
    # ctr += num
    # print(ctr / len(symbols) * 100, time.time())

    for symbol_subset in [symbols[i:i + num] for i in range(0, len(symbols), num)]:
        pool = mpool.ThreadPool(processes=16)
        results = pool.map(get_data_for_wrapper, [(symbol, 2006, 2016) for symbol in symbol_subset])
        for res in results:
            if len(csv_rows) != 0:
                # we already have the header
                res = res[1:]
            csv_rows.extend(res)
        ctr += 1
        print(num * ctr / len(symbols) * 100, time.time())

    with open("op.pkl", "wb") as op_f:
        pickle.dump(csv_rows, file=op_f)


main()
