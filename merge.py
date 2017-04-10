import pandas as pd
import pandas.io.common
import parse

import sys
import time

CSV_DIR = "csv"
CSV_FMT = CSV_DIR + "/%s.csv"
MERGED_OP_FILE = CSV_DIR + "/merged.csv"


def main():
    symbols = list(sorted(parse.get_symbols_to_fetch()))
    ctr = 0
    header = None
    rows = []
    for symbol in sorted(symbols):
        ctr += 1
        with open(CSV_FMT % symbol) as f:
            for line in f.readlines():
                line = line.strip()
                if header is None:
                    header = line
                elif line != header:
                    rows.append(line)

        print(ctr * 100 / len(symbols))

    with open(CSV_FMT % "merged", "w") as f:
        f.write(header + "\n")
        for row in rows:
            f.write(row + "\n")


if __name__ == '__main__':
    main()
