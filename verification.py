import data_util
import correlation

import pandas as pd
import numpy as np

import datetime
import pickle
import itertools
import time
import sys
import math
import warnings
import multiprocessing as mp
import os

warnings.simplefilter("error")

ctr = 0
tot = 0

NUM_CORES = 8


def analyse_corr(corr_pkl_file):
    with open(corr_pkl_file, "rb") as f:
        corr_list = pickle.load(f)
        corr_list = [list_item for list_item in corr_list if len(list_item[1]) != 0]
        for item in sorted(corr_list, key=lambda x: np.mean(list(map(lambda y: y[1], x[1])))):
            print(item)
        # print(max(map(lambda x: np.mean(x), corr_dict.values())))


def mp_get_corr(args):
    df1, df2 = args
    global ctr
    global tot
    ctr += 1
    if ctr % 100 == 0:
        print(ctr / tot * 100, os.getpid())
    return tuple(sorted((df1[data_util.KEY_SYMBOL].iloc[-1],
                         df2[data_util.KEY_SYMBOL].iloc[-1]))), correlation.get_correlation(df1, df2)


def main():
    global ctr
    global tot

    symbols_read_time = time.time()

    with open("symbols_df.pkl", "rb") as pkl_file:
        symbol_dfs = pickle.load(pkl_file)

    print("Time taken to read the symbols df pickle", time.time() - symbols_read_time, file=sys.stderr)
    symbol_dfs = [symbol_df for symbol_df in symbol_dfs if len(symbol_df.index) > 0]
    combs = itertools.combinations(symbol_dfs, 2)
    tot = len(symbol_dfs) * (len(symbol_dfs) - 1) // 2
    ctr = 0

    results = mp.Pool(processes=NUM_CORES).map(func=mp_get_corr, iterable=list(combs))
    # print(results)

    with open("avg_max_corrs.pkl", "wb") as pkl_file:
        pickle.dump(results, pkl_file)


if __name__ == '__main__':
    # main()

    analyse_corr("avg_max_corrs.pkl")
