import pandas as pd

import datetime
import time
import sys

KEY_SYMBOL = "Symbol"
_KEY_SERIES = "Series"
KEY_DATE = "Date"
KEY_OPEN_PRICE = "Open Price"


def read_csv(csv_fname):
    df = pd.read_csv(csv_fname)
    df = df[df[_KEY_SERIES] == "EQ"]
    df[KEY_DATE] = df[KEY_DATE].apply(lambda x: datetime.datetime.strptime(x, "%d-%b-%Y").date())
    # deduplicate data - this is NSE's fault
    # dedup_time = time.time()
    df = df[~df.duplicated(KEY_DATE)]
    # time taken = ~0.001s
    # print("Dedup time:", time.time() - dedup_time, file=sys.stderr)
    # print(csv_fname, df[KEY_DATE].nunique(), df[KEY_DATE].count())
    return df


def test():
    pass


if __name__ == '__main__':
    test()
