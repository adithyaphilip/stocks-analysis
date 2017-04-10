import data_util
import graph_utils
import correlation

import pickle
import datetime
import numpy as np


def main():
    df1 = data_util.read_csv("csv/IDFC.csv")
    df2 = data_util.read_csv("csv/PSUBNKBEES.csv")
    df1 = df1[df1[data_util.KEY_DATE].apply(lambda date: date.year == 2016)]
    df2 = df2[df2[data_util.KEY_DATE].apply(lambda date: date.year == 2016)]
    graph_utils.plot_line_graph(df1, df2, lag=datetime.timedelta(days=0))
    return
    for days in [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28]:
        corr1, corr2 = correlation.get_corr_with_lag(df1=data_util.read_csv("csv/IDFC.csv"),
                                                     df2=data_util.read_csv("csv/PSUBNKBEES.csv"),
                                                     lag=datetime.timedelta(days=days))

        avg1 = np.mean(list(map(lambda x: x[1], corr1))[-2:])
        avg2 = np.mean(list(map(lambda x: x[1], corr2))[-2:])

        print(max(avg1, avg2), avg1, avg2)


if __name__ == '__main__':
    main()
